# Can find this block of code in USE PROVIDER in terraform
# When we use command terraform init - terraform will look at this file and communicade to the specify provider
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.4.0"
    }
  }
}

provider "google" {
  # credentials = "path to key"
  # or export GOOGLE_CREDENTIALS="{Path to key}"
  project = "terraform-demo-441316" #found in project dashboard
  region  = "asia-southeast1" #https://cloud.google.com/docs/geography-and-regions -link for region
}

#what kind of resource we want to create, in this case is google_storage_bucket whick block name is demo-bucket
resource "google_storage_bucket" "demo-bucket" { 
  name          = "terraform-demo-441316-terra-bucket"
  location      = "asia"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

# terraform init - initialize connection.
# terraform plan - update plan (main.tf) in this case.
# terraform apply - deploy : .terraform.tfstate.lock.info will created during waiting for a confirmation
#                   and will be remove after we finish a comfirmation.


