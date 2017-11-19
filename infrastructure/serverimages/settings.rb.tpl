CORES = "1"
MEMORY = "512"
HOSTNAME = "zarya"

PORTS = {
  8080 => 80,
  8443 => 443,
  2202 => 22, # For ssh without messing with bridged device
}
