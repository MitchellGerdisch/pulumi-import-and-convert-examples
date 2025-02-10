resource "azurerm_resource_group" "rg" {
  name     = "my-uniquely-named-rg-020625"
  location = "centralus"
}


module "vnet" {
  source               = "./terraform-azurerm-vnet"
  resource_group_name  = azurerm_resource_group.rg.name
  location             = "centralus"
  vnet_name            = "new-vnet"
  vnet_address_space   = "10.10.0.0/16"
  subnet_name          = "subnet01"
  subnet_address_space = "10.10.10.0/24"
}

module "vnet2" {
  source               = "./terraform-azurerm-vnet"
  resource_group_name  = azurerm_resource_group.rg.name
  location             = "centralus"
  vnet_name            = "new-vnet2"
  vnet_address_space   = "10.10.0.0/16"
  subnet_name          = "subnetb01"
  subnet_address_space = "10.10.10.0/24"
}

