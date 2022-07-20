# Import our service's bus client
from bus import bus

# Call the check_password() procedure on our auth API
status = bus.getLantStatus.get()

print(status)