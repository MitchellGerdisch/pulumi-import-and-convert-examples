import pulumi
import pulumi_azure_native as azure_native

my_imported_rg = azure_native.resources.ResourceGroup("my-imported-rg",
    location="westus2",
    resource_group_name="resource_group2c255dc1",
    opts = pulumi.ResourceOptions(protect=True))

my_imported_sa = azure_native.storage.StorageAccount("my-imported-sa",
    access_tier=azure_native.storage.AccessTier.HOT,
    account_name="storageaccount201966e8",
    allow_blob_public_access=False,
    allow_cross_tenant_replication=False,
    enable_https_traffic_only=True,
    encryption={
        "key_source": azure_native.storage.KeySource.MICROSOFT_STORAGE,
        "services": {
            "blob": {
                "enabled": True,
                "key_type": azure_native.storage.KeyType.ACCOUNT,
            },
            "file": {
                "enabled": True,
                "key_type": azure_native.storage.KeyType.ACCOUNT,
            },
        },
    },
    kind=azure_native.storage.Kind.STORAGE_V2,
    location="westus2",
    minimum_tls_version=azure_native.storage.MinimumTlsVersion.TLS1_0,
    network_rule_set={
        "bypass": azure_native.storage.Bypass.AZURE_SERVICES,
        "default_action": azure_native.storage.DefaultAction.ALLOW,
    },
    resource_group_name=my_imported_rg.name,
    sku={
        "name": azure_native.storage.SkuName.STANDARD_LRS,
    },
    opts = pulumi.ResourceOptions(protect=True))

my_imported_blobcontainer = azure_native.storage.BlobContainer("my-imported-blobcontainer",
    account_name=my_imported_sa.name,
    container_name="blobcontainer",
    default_encryption_scope="$account-encryption-key",
    deny_encryption_scope_override=False,
    public_access=azure_native.storage.PublicAccess.NONE,
    resource_group_name=my_imported_rg.name,
    opts = pulumi.ResourceOptions(protect=True))
