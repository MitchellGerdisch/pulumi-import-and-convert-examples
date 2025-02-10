variable "vnet_name" {
  type        = string
  description = "Name of the vNet"
}

variable "resource_group_name" {
  type        = string
  description = "Name of the resource group"
}

variable "location" {
  type        = string
  description = "Location of the resource group"
}

variable "vnet_address_space" {
  type        = string
  description = "Address space of the vNet" 
}

variable "subnet_name" {
  type        = string  
  description = "Name of the subnet"  
}

variable "subnet_address_space" {
  type        = string  
  description = "Address space of the subnet"
}
