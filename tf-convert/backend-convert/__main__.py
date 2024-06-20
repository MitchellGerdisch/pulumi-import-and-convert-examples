import pulumi
import pulumi_azure as azure
import pulumi_azuread as azuread
import pulumi_terraform as terraform


def not_implemented(msg):
    raise NotImplementedError(msg)

config = pulumi.Config()
managed_identity_principal_id = config.get_object("managedIdentityPrincipalId")
if managed_identity_principal_id is None:
    managed_identity_principal_id = None
roles = azuread.get_directory_roles_output()
ad_role_names = not_implemented("""toset([
"User Administrator",
"Groups Administrator",
"Application Administrator",
])""")
ad_roles = roles.apply(lambda roles: {r.display_name: r.object_id for r in roles.roles})
roles_keeper = terraform.index.Data("roles_keeper", triggers_replace=ad_roles)
state_rg = azure.core.ResourceGroup("state_rg",
    location="eastus",
    name="bambrane-runner-state")
bambrane_operator = azure.authorization.UserAssignedIdentity("bambrane_operator",
    location=state_rg.location,
    name="bambrane_operator",
    resource_group_name=state_rg.name)
role_binding = []
for range in [{"value": i} for i in range(0, ad_role_names)]:
    role_binding.append(azuread.DirectoryRoleAssignment(f"role_binding-{range['value']}",
        directory_scope_id="/",
        role_id=ad_roles[range["value"]],
        principal_object_id=bambrane_operator.principal_id))
onees_rm = azuread.get_service_principal_output(display_name="1ES Resource Management")
vnet = azure.network.VirtualNetwork("vnet",
    address_spaces=["192.168.0.0/16"],
    location=state_rg.location,
    name="control-plane-meta-controller",
    resource_group_name=state_rg.name)
runner = azure.network.Subnet("runner",
    address_prefixes=["192.168.128.0/24"],
    name="private",
    resource_group_name=state_rg.name,
    virtual_network_name=vnet.name,
    service_endpoints=["Microsoft.Storage"])
bambrane_onees_pool = azure.network.Subnet("bambrane_onees_pool",
    address_prefixes=["192.168.100.0/24"],
    name="runner",
    resource_group_name=state_rg.name,
    virtual_network_name=vnet.name,
    delegations=[azure.network.SubnetDelegationArgs(
        name="delegation",
        service_delegation=azure.network.SubnetDelegationServiceDelegationArgs(
            name="Microsoft.CloudTest/hostedpools",
            actions=["Microsoft.Network/virtualNetworks/subnets/join/action"],
        ),
    )])
endpoints = not_implemented("toset([\"blob\"])")
pulumi.export("virtualNetworkId", vnet.id)
pulumi.export("subnetId", runner.id)
current = azure.core.get_client_config_output()
state_storage = azure.keyvault.KeyVault("state_storage",
    name="azmodbackend",
    location=state_rg.location,
    resource_group_name=state_rg.name,
    tenant_id=current.tenant_id,
    soft_delete_retention_days=7,
    purge_protection_enabled=True,
    sku_name="standard")
state_storage_account = azure.authorization.UserAssignedIdentity("state_storage_account",
    location=state_rg.location,
    name="state-storage-account",
    resource_group_name=state_rg.name)
identity = azure.keyvault.AccessPolicy("identity",
    key_vault_id=state_storage.id,
    object_id=state_storage_account.principal_id,
    tenant_id=state_storage_account.tenant_id,
    key_permissions=[
        "Get",
        "UnwrapKey",
        "WrapKey",
    ])
current_user = azure.keyvault.AccessPolicy("current_user",
    key_vault_id=state_storage.id,
    object_id=not_implemented("coalesce(var.managed_identity_principal_id,data.azurerm_client_config.current.object_id)"),
    tenant_id=current.tenant_id,
    key_permissions=[
        "Get",
        "Recover",
        "Create",
        "Delete",
        "GetRotationPolicy",
    ])
storage_encryption_key = azure.keyvault.Key("storage_encryption_key",
    key_opts=[
        "decrypt",
        "encrypt",
        "sign",
        "unwrapKey",
        "verify",
        "wrapKey",
    ],
    key_type="RSA",
    key_vault_id=state_storage.id,
    name="storageaccount",
    key_size=2048)
state = azure.storage.Account("state",
    account_replication_type="ZRS",
    account_tier="Standard",
    account_kind="StorageV2",
    location=state_rg.location,
    name="tfmod1espoolstatestorage",
    resource_group_name=state_rg.name,
    public_network_access_enabled=True,
    customer_managed_key=azure.storage.AccountCustomerManagedKeyArgs(
        key_vault_key_id=storage_encryption_key.id,
        user_assigned_identity_id=state_storage_account.id,
    ),
    identity=azure.storage.AccountIdentityArgs(
        type="UserAssigned",
        identity_ids=[state_storage_account.id],
    ))
state_resource = azure.storage.Container("state",
    name="azure-verified-tfmod-runner-state",
    storage_account_name=state.name,
    container_access_type="private")
plan = azure.storage.Container("plan",
    name="azure-verified-tfmod-pull-request-plans",
    storage_account_name=state.name,
    container_access_type="private")
bambrane_provision_script = azure.storage.Account("bambrane_provision_script",
    account_replication_type="ZRS",
    account_tier="Standard",
    account_kind="StorageV2",
    location=state_rg.location,
    name="bambraneprovisionscript",
    resource_group_name=state_rg.name,
    public_network_access_enabled=True,
    customer_managed_key=azure.storage.AccountCustomerManagedKeyArgs(
        key_vault_key_id=storage_encryption_key.id,
        user_assigned_identity_id=state_storage_account.id,
    ),
    identity=azure.storage.AccountIdentityArgs(
        type="UserAssigned",
        identity_ids=[state_storage_account.id],
    ))
#Azure Active Directory authorization must be enabled for your blob storage container.
#Authentication method must be set to Azure AD User Account for your container
#For now I cannot find the corresponding Terraform argument yet, I set this argument via GUI.
provision_script = azure.storage.Container("provision_script",
    name="onees-provison-script",
    storage_account_name=bambrane_provision_script.name,
    container_access_type="private")
provision_script_resource = azure.storage.Blob("provision_script",
    name="Setup.sh",
    storage_account_name=bambrane_provision_script.name,
    storage_container_name=provision_script.name,
    type="Block",
    access_tier="Cool",
    content_type="text/x-sh",
    source_content=bambrane_operator.principal_id.apply(lambda principal_id: f"echo MSI_ID=\"{principal_id}\" >> /etc/environment"))
onees_rm_blob_reader = azure.authorization.Assignment("onees_rm_blob_reader",
    principal_id=onees_rm.object_id,
    scope=bambrane_provision_script.id,
    role_definition_name="Storage Blob Data Reader")
storage_accounts = {
    "state": state.id,
    "provisionScript": bambrane_provision_script.id,
}
storage_contributor = []
def create_storage_contributor(range_body):
    for range in [{"key": k, "value": v} for [k, v] in enumerate(range_body)]:
        storage_contributor.append(azure.authorization.Assignment(f"storage_contributor-{range['key']}",
            principal_id=bambrane_operator.principal_id,
            scope=range["value"],
            role_definition_name="Storage Blob Data Contributor"))

storage_accounts.apply(create_storage_contributor)
this = azure.core.get_client_config_output()
subscription_contributor = azure.authorization.Assignment("subscription_contributor",
    principal_id=bambrane_operator.principal_id,
    scope=this.apply(lambda this: f"/subscriptions/{this.subscription_id}"),
    role_definition_name="Contributor")
