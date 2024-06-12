
resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = "mitch-tf-rg-import"
}

# Create a Storage Account within the Resource Group
resource "azurerm_storage_account" "sa" {
  name                     = "mitchtfsa"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Create a Storage Container within the Storage Account
resource "azurerm_storage_container" "sc" {
  name                  = "mitch-tf-sc"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}