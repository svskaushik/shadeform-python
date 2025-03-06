import os
import sys
import json

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shadeform import ShadeformClient

# Rest of your code remains unchanged
def main():
    # Get API key from environment variable or command line argument
    api_key = os.environ.get("SHADEFORM_API_KEY")
    
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        
    if not api_key:
        print("Error: Please provide an API key either as an environment variable SHADEFORM_API_KEY or as a command-line argument")
        sys.exit(1)
    
    # Initialize the Shadeform client
    client = ShadeformClient(api_key=api_key)
    
    try:
        # Call the instances/types endpoint
        print("Fetching instance types...")
        instance_types = client.instances.list_types()
        
        # Pretty print the response
        print("\nAvailable Instance Types:")
        print(json.dumps(instance_types, indent=2))
        
        # Optional: Format and display in a more readable way
        # if instance_types:
        #     print("\n=== Summary ===")
        #     for instance_type in instance_types:
        #         name = instance_type.get("name", "Unknown")
        #         gpu = instance_type.get("gpu", "N/A")
        #         description = instance_type.get("description", "")
        #         price = instance_type.get("price", {}).get("hourly", "N/A")
                
        #         print(f"- {name}: {gpu} {description} (${price}/hour)")
                
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()