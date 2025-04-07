## S3 Storage Bucket
resource "aws_s3_bucket" "storage_bucket" {
  bucket = "ds-storage-bucket-123"

  tags = {
    Name        = "storage_bucket"
    Environment = "Dev"
    Description = "S3 bucket to store data of people details."
  }
}

## Upload people_data.csv File to Storage Bucket
resource "aws_s3_object" "people_data_csv_file_upload" {
  bucket = "ds-storage-bucket-123"
  key    = "people_data.csv"
  source      = "${path.module}/../test/people_data.csv"
  source_hash = filemd5("${path.module}/../test/people_data.csv")
}

## S3 Target Bucket
resource "aws_s3_bucket" "target_bucket" {
  bucket = "ds-target-bucket-123"

  tags = {
    Name        = "target_bucket"
    Environment = "Dev"
    Description = "S3 bucket to store obfuscated data."
  }
}