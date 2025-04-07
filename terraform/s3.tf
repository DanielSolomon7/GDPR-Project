## S3 Storage Bucket
resource "aws_s3_bucket" "storage_bucket" {
  bucket = "ds-storage-bucket-123"

  tags = {
    Name        = "storage_bucket"
    Environment = "Dev"
    Description = "S3 bucket to store data of people details."
  }
}