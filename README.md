# Movie-list-downloader-optimizeer
python script for optimized movie downloader
How to Run download_movies.py from GitHub (Mac)
Follow these simple steps to clone the repository and run the script locally.

1️⃣ Open Terminal
Press Cmd + Space, type Terminal, and hit Enter.

2️⃣ Clone the GitHub Repository
Run the following command to download the repository:

bash
Copy
Edit
git clone https://github.com/Adamebaruch/Movie-list-downloader-optimizeer.git
Then, navigate into the cloned folder:

bash
Copy
Edit
cd Movie-list-downloader-optimizeer
3️⃣ Install Required Python Libraries
Your script requires some Python packages to work correctly. Install them using:

bash
Copy
Edit
pip3 install -r requirements.txt
If requirements.txt is missing, manually install the required packages:

bash
Copy
Edit
pip3 install beautifulsoup4 requests qbittorrent-api pandas
4️⃣ Run the Script
Once everything is set up, run the script with:

bash
Copy
Edit
python3 download_movies.py
5️⃣ (Optional) Enable qBittorrent Web UI
If qBittorrent is required for downloads:

Install qBittorrent if not already installed:
🔗 Download qBittorrent
Open qBittorrent and go to Tools → Preferences → Web UI.
Enable the Web UI and set a username/password.
6️⃣ Done! 🎉
Now, the script will start searching for movies and downloading torrents via qBittorrent.

Quick Summary
Open Terminal.
Clone the repository:
bash
Copy
Edit
git clone https://github.com/Adamebaruch/Movie-list-downloader-optimizeer.git
cd Movie-list-downloader-optimizeer
Install dependencies:
bash
Copy
Edit
pip3 install -r requirements.txt
Run the script:
bash
Copy
Edit
python3 download_movies.py
That’s it! 🚀 Let me know if you need any modifications.
