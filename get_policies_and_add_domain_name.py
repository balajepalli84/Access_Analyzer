import oci
import re

# Create a default configuration from the config file
config = oci.config.from_file()

# Initialize the IdentityClient with the config
identity_client = oci.identity.IdentityClient(config)

# Set the compartment ID to the tenancy ID
compartment_id = config["tenancy"]

# Set the output file path
output_file = r'C:\Security\Blogs\Access_Analyzer\logs\policies.txt'

# Function to format the group name
def format_group_name(statement):
    # Regular expression to find the group name after "allow group "
    match = re.search(r'allow group (\S+)', statement)
    if match:
        group_name = match.group(1)
        if '/' in group_name:
            domain, group = group_name.split('/', 1)
            # Check if the domain and group are already enclosed in quotes
            if not (domain.startswith("'") and domain.endswith("'")):
                domain = f"'{domain}'"
            if not (group.startswith("'") and group.endswith("'")):
                group = f"'{group}'"
            formatted_group = f"{domain}/{group}"
        else:
            # Add 'default'/'groupname' if no domain is present
            if not (group_name.startswith("'") and group_name.endswith("'")):
                formatted_group = f"'default'/'{group_name}'"
            else:
                formatted_group = f"'default'/{group_name}"
        # Replace the original group name with the formatted one
        return statement.replace(group_name, formatted_group)
    return statement

# List policies in the compartment
policies = identity_client.list_policies(compartment_id)

# Open the file in write mode
with open(output_file, 'w') as file:
    for policy in policies.data:
        # Filter and format statements
        filtered_statements = [
            format_group_name(statement.lower()) 
            for statement in policy.statements if 'allow group' in statement.lower()
        ]
        
        if filtered_statements:
            file.write(f"Policy Name: {policy.name}\n")
            file.write("Filtered Statements:\n")
            for statement in filtered_statements:
                file.write(f"  - {statement}\n")
            file.write('\n')

print(f"Filtered policy statements have been written to {output_file}")
