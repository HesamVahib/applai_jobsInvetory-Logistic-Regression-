from supabase import create_client, Client
import os

# ------------ Load environment variables ------------
# from dotenv import load_dotenv

# load_dotenv()

# supabase_url = os.getenv('SUPABASE_URL')
# supabase_key = os.getenv('SUPABASE_KEY')
# ---------------------------------------------------

supabase_url = os.environ["SUPABASE_URL"]
supabase_key = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(supabase_url, supabase_key)

if __name__ == "__main__":
    try:
        response = supabase.table('jobs').select("*", count="exact").execute()
        print(response)
        print(f"✅ Successfully connected to jobs table, found {response.count} records.")
    except Exception as e:
        print(f"❌ Failed to connect to jobs table: {e}")

    try:
        response = supabase.table('jobs').insert({
            "title": "Test",
            "location": "Helsinki",
            "category": "Technology",
            "company": "New Company",
            "link": "https://example.com/new-job",
            "fi_lang": "Finnish",
            "en_lang": "English"
        }).execute()
        print(f"✅ Successfully inserted a new job: {response.data}")
    except Exception as e:
        print(f"❌ Failed to insert a new job: {e}")