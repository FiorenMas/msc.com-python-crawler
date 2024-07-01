import aiohttp
import asyncio

async def fetch_data(session, url, tracking_number):
    async with session.post(url, json={"trackingNumber": tracking_number, "trackingMode": "0"}) as response:
        return await response.json()

async def main():
    url = "https://www.msc.com/api/feature/tools/TrackingInfo"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,vi;q=0.7,en;q=0.3",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

    tracking_number = input("Enter the tracking number: ")

    async with aiohttp.ClientSession(headers=headers) as session:
        result = await fetch_data(session, url, tracking_number)
        if result.get('IsSuccess'):
            data = result.get('Data', {})
            bill_of_ladings = data.get('BillOfLadings', [])
            if bill_of_ladings:
                general_info = bill_of_ladings[0].get('GeneralTrackingInfo', {})
                print(f"Shipped From: {general_info.get('ShippedFrom')}")
                print(f"Shipped To: {general_info.get('ShippedTo')}")
                print(f"Port of Load: {general_info.get('PortOfLoad')}")
                print(f"Port of Discharge: {general_info.get('PortOfDischarge')}")
                print(f"Price Calculation Date: {general_info.get('PriceCalculationDate')}")

                export_event = next((event for container_info in bill_of_ladings[0].get('ContainersInfo', [])
                                     for event in container_info.get('Events', [])
                                     if event['Description'] == 'Export Loaded on Vessel'), None)
                import_event = next((event for container_info in bill_of_ladings[0].get('ContainersInfo', [])
                                     for event in container_info.get('Events', [])
                                     if event['Description'] == 'Import Discharged from Vessel'), None)

                if export_event:
                    print(f"Export Loaded on Vessel: {export_event['Date']}")
                if import_event:
                    print(f"Import Discharged from Vessel: {import_event['Date']}")
            else:
                print("No tracking information found.")
        else:
            print("Error fetching tracking data.")

if __name__ == "__main__":
    asyncio.run(main())
