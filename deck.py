from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Path to your client secrets file
client_secrets_path = 'C:\\Users\\MICHEL\\OneDrive\\Desktop\\Ruralidays Test Cases\\Google_Slides_API\\credentials.json'

# Scopes you need
scopes = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']

# Set up the OAuth2 flow
flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, scopes)

# Prompt the user to authenticate
creds = flow.run_local_server(port=0)

# Build the Slides API client
slides_service = build('slides', 'v1', credentials=creds)

# Build the Drive API client
drive_service = build('drive', 'v3', credentials=creds)

# The template presentation ID
template_presentation_id = '1gf2iPyKUPxzy4_pZcQBcwT45ST40W3HSK1hF7d9DMio'

# Slide options
slide_options = {
    "1": {"id": "g25f292d29b1_0_61", "description": "Cover"},
    "2": {"id": "g25f292d29b1_0_248", "description": "Introduction"},
    "3": {"id": "g25f292d29b1_0_374", "description": "Exterior"},
    "4": {"id": "g25f292d29b1_0_434", "description": "Cesped"}
}

print("Select the slides you want to include:")
for option, slide_info in slide_options.items():
    print(f"{option}. {slide_info['description']}")

selected_options = input("Enter numbers separated by commas: ").split(",")

# Get selected slide IDs
selected_slide_ids = [slide_options[option.strip()]['id'] for option in selected_options]

# Define the dynamic title
nombre_casa = "Your House Name Here"  # Replace with the actual house name
dynamic_title = f"Recomendaciones {nombre_casa}"

# Copy the template presentation
copy_request = {
    'name': dynamic_title
}
copy_response = drive_service.files().copy(
    fileId=template_presentation_id,
    body=copy_request
).execute()

# The new presentation ID
new_presentation_id = copy_response['id']

# Get all slide IDs
presentation = slides_service.presentations().get(presentationId=new_presentation_id).execute()
all_slide_ids = [slide['objectId'] for slide in presentation['slides']]

# Delete unselected slides
delete_requests = [{'deleteObject': {'objectId': slide_id}} for slide_id in all_slide_ids if slide_id not in selected_slide_ids]
slides_service.presentations().batchUpdate(presentationId=new_presentation_id, body={'requests': delete_requests}).execute()

# The new presentation URL
new_presentation_url = f"https://docs.google.com/presentation/d/{new_presentation_id}/edit"

print(f"New presentation created. URL: {new_presentation_url}")

# Your requests to replace placeholders (as previously described)
requests = [
    {
        'replaceAllText': {
            'containsText': {
                'text': '{{NOMBRE CASA}}',
                'matchCase': False
            },
            'replaceText': 'Your New Text Here',
            'pageObjectIds': selected_slide_ids
        }
    }
]

# Perform the batch update on the new presentation
body = {'requests': requests}
response = slides_service.presentations().batchUpdate(presentationId=new_presentation_id, body=body).execute()

print(response)
