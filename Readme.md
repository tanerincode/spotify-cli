# 🎵 Spotify CLI – Automate Your Playlists 🚀

A command-line tool to **create playlists**, **add songs**, and **clean up duplicates** on Spotify. No more manual searching—just run a command and let the magic happen! 🎶🔥  

## 📌 Features
👉 Create new Spotify playlists  
👉 Add songs from a text file  
👉 Prevent duplicate songs from being added  
👉 Cleanup function to remove duplicate tracks  
👉 Fully **automated** with **Spotify**  

---

## ⚡️ Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/tanerincode/spotify-cli.git
cd spotify-cli
```

### **2️⃣ Install Dependencies**
Make sure you have Python **3.7+** installed, then install the required libraries:

```sh
pip install -r requirements.txt
```

### **3️⃣ Setup Spotify API Credentials**
Create a `.env` file in the root directory and add your **Spotify API credentials**:

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```

To get your **Spotify Client ID & Secret**, create an app at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).

---

### **4️⃣ Create a Global Symlink**
To make the CLI accessible from anywhere, create a symlink:
```sh
sudo ln -s $(pwd)/spotify_cli.py /usr/local/bin/spotify-cli
```
Now you can use `spotify-cli` globally.

---

## 🚀 Usage

### **Create a New Playlist**
```sh
spotify-cli create-playlist "My Awesome Playlist"
```

### **Add Songs from a File**
Create a text file (e.g., `songs.txt`) with song names:
```
Bob Marley – One Love
Damian Marley – Welcome to Jamrock
Toots & The Maytals – Monkey Man
```
Then run:
```sh
spotify-cli add-songs "My Awesome Playlist" songs.txt
```

### **Cleanup Duplicates in a Playlist**
```sh
spotify-cli cleanup "My Awesome Playlist"
```

---

## 💪 Contributing
Pull requests are welcome! Feel free to improve features, optimize performance, or suggest new ideas. 🚀

## 📝 License
This project is licensed under the MIT License. See `LICENSE` for details.

---

🎶 **Enjoy automating your Spotify experience!** 🎶🔥
