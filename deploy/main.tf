terraform {
  backend "azurerm" {
    resource_group_name  = "base-infrastructure-terraform"
    key                  = "metadata-finder.tfstate"
    storage_account_name = "delphaidevelopment"
    container_name       = "delphai-development-terraform-state"
  }
}
module "delphai-app" {
  source      = "git@github.com:delphai/infrastructure.git//modules/delphai-app"
  app_port    = 8000
  delphai_env = "development"
  image       = "delphaidevelopment.azurecr.io/metadata-finder"
  name        = "metadata-finder"
  namespace   = "default"
  subdomain   = "api"
  path        = "/metadata-finder"
}
