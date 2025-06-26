resource "aws_dynamodb_table" "articles" {
  name         = "articles"
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "title"
  range_key = "date"

  attribute {
    name = "title"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }

  tags = {
    Project     = "readability-articles"
  }
}
