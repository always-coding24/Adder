# Beginner’s Guide: Running Adder on Termux

This guide will help you (even if you are not tech-savvy) to set up everything needed to run the Adder Python script on your Android device using Termux.

---

## 1. Install Termux on Your Android Device

1. Open the **Google Play Store** or **F-Droid** app.
2. Search for **Termux**.
3. Install **Termux**.

---

## 2. Open Termux and Update the Package List

Type each line below and press **Enter** after each one:

```bash
pkg update
pkg upgrade
```

If asked to continue, type `y` and press Enter.

---

## 3. Install Git and Python

Type this command and press **Enter**:

```bash
pkg install git python -y
```

---

## 4. Clone the Adder Project from GitHub

Type:

```bash
git clone https://github.com/always-coding24/Adder.git
```

---

## 5. Change Directory to the Project Folder

Type:

```bash
cd Adder
```

---

## 6. Install the Required Python Libraries

Type the following command and press **Enter**:

```bash
pip install requests bs4
```

---

## 7. Run the add.py Script

Type:

```bash
python add.py
```

---

## 8. Follow On-Screen Instructions

- The script will ask for the number range you want to add.
- Type the range name and press **Enter**.
- To stop, type `exit` and press **Enter**.

---

## Troubleshooting

- If you get an error about missing pip, run:  
  ```bash
  pkg install python
  ```
  Then try the pip install command again.

- If you see any other error, copy the error message and ask for help.

---

## Summary of All Commands

You can copy and paste each line one-by-one into Termux:

```bash
pkg update
pkg upgrade
pkg install git python -y
git clone https://github.com/always-coding24/Adder.git
cd Adder
pip install requests bs4
python add.py
```

---

## Done!

You now have everything set up to use the Adder script on your Android device.
