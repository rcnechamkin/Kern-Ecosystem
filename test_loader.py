from datetime import datetime
from filing_cabinet import loader

start = datetime(2025, 6, 2)
end = datetime(2025, 6, 9)

entries = loader.get_entries_between("journals", start, end)
print(f"Found {len(entries)} journal entries between {start.date()} and {end.date()}:\n")
for entry in entries:
    print(entry)
