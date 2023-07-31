data "archive_file" "lambda-function-data-zip" {
	type             = "zip"
	source_file      = "${path.module}/lambda/app.py"
	output_path      = "${path.module}/lambda/lambda-my-function.zip"
}

resource "aws_lambda_function" "ec2_lambda" {
	filename      = data.archive_file.lambda-function-data-zip.output_path
	function_name = "ec2_with_lambda"
	role          = aws_iam_role.lambda-role-for-access-ec2-and-cloudwatch.arn
	handler       = "app.lambda_handler"
	source_code_hash 	= data.archive_file.lambda-function-data-zip.output_base64sha256
	runtime 			= "python3.9"
	layers			= [aws_lambda_layer_version.lambda_layer.arn]

	tracing_config {
		mode = "Active"
	}

	depends_on = [
		aws_lambda_layer_version.lambda_layer,
		data.archive_file.lambda-function-data-zip
	]
}

resource "aws_lambda_layer_version" "lambda_layer" {
	description = "Layer to use pretty table"
  	filename   = "${path.module}/aws-dist/challege-cocus-0.0.1.zip"
  	layer_name = "challege-cocus"
  	compatible_architectures = ["x86_64"]
  	compatible_runtimes = ["python3.9"]
}

resource "aws_lambda_invocation" "example" {
  function_name = aws_lambda_function.ec2_lambda.function_name

  input = jsonencode({
    instance_id = ""
  })
}

output "result_entry" {
  value = jsondecode(aws_lambda_invocation.example.result)["body"]
}