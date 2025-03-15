"""
Example usage of the Shadeform SDK corresponding to the raw API endpoint examples.
This demonstrates how to use the SDK for GET requests to various resources.
"""

import os
import sys
import json
sys.path.insert(0, '/Users/lpcadmin/Documents/Projects/shadeform')
from shadeform import ShadeformClient

# Initialize the client
api_key = os.environ.get("SHADEFORM_API_KEY", "your-api-key-here")
client = ShadeformClient(api_key=api_key)

# Helper function to pretty print JSON
def print_json(data):
    print(json.dumps(data, indent=2))

# ----- INSTANCES -----

# Get instance info
def get_instance_info(instance_id):
    """Get information about a specific instance."""
    print(f"\n===== Getting info for instance {instance_id} =====")
    instance = client.instances.get_info(instance_id)
    print("\nRaw response:")
    print_json(instance)
    return instance

# List all instances
def list_instances():
    """List all instances."""
    print("\n===== Listing all instances =====")
    instances = client.instances.list_all()
    print("\nRaw response:")
    print_json(instances)
    
    print(f"\nFound {len(instances)} instances")
    for instance in instances:
        instance_id = instance.get('id', 'N/A')
        instance_name = instance.get('name', 'N/A')
        instance_status = instance.get('status', 'N/A')
        print(f"- {instance_id}: {instance_name} ({instance_status})")
    
    return instances

# List available instance types
def list_instance_types():
    """List available instance types."""
    print("\n===== Listing available instance types =====")
    instance_types = client.instances.list_types()
    print("\nRaw response (first 2 items):")
    if instance_types and len(instance_types) > 0:
        print_json(instance_types[:2])
    else:
        print_json(instance_types)
    
    print(f"\nFound {len(instance_types)} instance types")
    for instance_type in instance_types:
        # Debug: Print the structure of the first item to understand the schema
        if instance_types.index(instance_type) == 0:
            print("\nFirst instance type structure:")
            print_json(instance_type)
            
        # Try different fields that might contain the instance type name
        type_name = instance_type.get('shade_instance_type') or instance_type.get('type') or 'N/A'
        provider = instance_type.get('cloud') or instance_type.get('provider') or 'N/A'
        price = instance_type.get('hourly_price', 'N/A')
        
        print(f"- {type_name}: {provider} ({price}/hr)")
    
    return instance_types

# ----- SSH KEYS -----

# Get SSH key info
def get_ssh_key_info(key_id):
    """Get information about a specific SSH key."""
    print(f"\n===== Getting info for SSH key {key_id} =====")
    key = client.ssh_keys.get_info(key_id)
    print("\nRaw response:")
    print_json(key)
    # Note: If key doesn't exist, this will return an empty dictionary ({}) not None
    return key

# List all SSH keys
def list_ssh_keys():
    """List all SSH keys."""
    print("\n===== Listing all SSH keys =====")
    keys = client.ssh_keys.list_all()
    print("\nRaw response:")
    print_json(keys)
    
    print(f"\nFound {len(keys)} SSH keys")
    for key in keys:
        key_id = key.get('id', 'N/A')
        key_name = key.get('name', 'N/A')
        print(f"- {key_id}: {key_name}")
    
    return keys

# ----- VOLUMES -----

# Get volume info
def get_volume_info(volume_id):
    """Get information about a specific volume."""
    print(f"\n===== Getting info for volume {volume_id} =====")
    volume = client.volumes.get_info(volume_id)
    print("\nRaw response:")
    print_json(volume)
    return volume

# List all volumes
def list_volumes():
    """List all volumes."""
    print("\n===== Listing all volumes =====")
    volumes = client.volumes.list_all()
    print("\nRaw response:")
    print_json(volumes)
    
    print(f"\nFound {len(volumes)} volumes")
    for volume in volumes:
        volume_id = volume.get('id', 'N/A')
        volume_name = volume.get('name', 'N/A')
        volume_size = volume.get('size_gb', 'N/A')
        print(f"- {volume_id}: {volume_name} ({volume_size}GB)")
    
    return volumes

# List available volume types
def list_volume_types():
    """List available volume types."""
    print("\n===== Listing available volume types =====")
    volume_types = client.volumes.list_types()
    print("\nRaw response (first 2 items):")
    if volume_types and len(volume_types) > 0:
        print_json(volume_types[:2])
    else:
        print_json(volume_types)
    
    print(f"\nFound {len(volume_types)} volume types")
    for volume_type in volume_types:
        # Debug: Print the structure of the first item
        if volume_types.index(volume_type) == 0:
            print("\nFirst volume type structure:")
            print_json(volume_type)
            
        name = volume_type.get('name') or volume_type.get('type') or 'N/A'
        description = volume_type.get('description', 'N/A')
        print(f"- {name}: {description}")
    
    return volume_types

# ----- TEMPLATES -----

# Get template info
def get_template_info(template_id):
    """Get information about a specific template."""
    print(f"\n===== Getting info for template {template_id} =====")
    template = client.templates.get_info(template_id)
    print("\nRaw response:")
    print_json(template)
    return template

# List all templates
def list_templates():
    """List all templates."""
    print("\n===== Listing all templates =====")
    templates = client.templates.list_all()
    print("\nRaw response:")
    print_json(templates)
    
    print(f"\nFound {len(templates)} templates")
    for template in templates:
        template_id = template.get('id', 'N/A')
        template_name = template.get('name', 'N/A')
        template_desc = template.get('description', 'N/A')
        print(f"- {template_id}: {template_name} ({template_desc})")
    
    return templates

# List featured templates
def list_featured_templates():
    """List featured templates."""
    print("\n===== Listing featured templates =====")
    # Using list_featured instead of get_featured to match the actual SDK method name
    featured = client.templates.list_featured()
    print("\nRaw response:")
    print_json(featured)
    
    print(f"\nFound {len(featured)} featured templates")
    for template in featured:
        template_id = template.get('id', 'N/A')
        template_name = template.get('name', 'N/A')
        print(f"- {template_id}: {template_name}")
    
    return featured

# Example usage
if __name__ == "__main__":
    # You can uncomment and run these functions with real IDs
    list_instances()
    # get_instance_info("instance-123")
    list_instance_types()
    
    list_ssh_keys()
    # get_ssh_key_info("key-123")
    
    list_volumes()
    # get_volume_info("vol-123")
    list_volume_types()
    
    # list_templates()
    # get_template_info("tmpl-123")
    # list_featured_templates()
    
    print("\nCompleted all API calls.")