# A (simple) component resource that creates an Azure Storage Account and Blob Container.

import pulumi
import pulumi_azure_native as azure_native

class StorageComponent(pulumi.ComponentResource):
    def __init__(self, name: str, resource_group_name: str, sa_name: str, opts: pulumi.ResourceOptions = None):
        super().__init__('mycomponent:az:StorageComponent', name, {}, opts)

        # Create an Azure Storage Account
        self.account = azure_native.storage.StorageAccount(
            "storageaccount",
            account_name=sa_name,
            resource_group_name=resource_group_name,
            sku=azure_native.storage.SkuArgs(
                name=azure_native.storage.SkuName.STANDARD_LRS,
            ),
            kind=azure_native.storage.Kind.STORAGE_V2,
            opts=pulumi.ResourceOptions(parent=self)
        )

        # Create a Blob Container
        self.blob_container = azure_native.storage.BlobContainer(
            "blobcontainer",
            account_name=self.account.name,
            resource_group_name=resource_group_name,
            public_access=azure_native.storage.PublicAccess.NONE,
            opts=pulumi.ResourceOptions(parent=self)
        )

        # Register the outputs
        self.register_outputs({
            'account': self.account,
            'blob_container': self.blob_container,
        })