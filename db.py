from supabase import create_client, Client

url: str = "DATABASE_URL"
key: str = "your_anon_public_key"
supabase: Client = create_client(url, key)

# Assuming you've already parsed titles and prices
for title, price in books:
    data = {"title": title, "price": price}
    supabase.table('books').insert(data).execute()
