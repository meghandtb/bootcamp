output "node_a_private_ip" {
  value = aws_instance.node-a.private_ip
}

output "node_b_private_ip" {
  value = aws_instance.node-b.private_ip
}
