# Browser Data Extraction Scripts

This repository contains a set of Python scripts that allow you to extract various types of data from web browsers, including **bookmarks**, **passwords**, **cache**, **cookies**, **downloads**, and **history**. The data is extracted from popular browsers like **Google Chrome**, **Brave**, **Mozilla Firefox**, and **Microsoft Edge** on Windows, macOS, and Linux operating systems.

## Table of Contents
1. [Overview](#overview)
2. [Supported Browsers](#supported-browsers)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Output](#output)


## Overview
This set of scripts allows you to extract browsing data such as:
- **Bookmarks**: Extract and view saved browser bookmarks.
- **Passwords**: Extract stored passwords from browsers.
- **Cache**: Extract cache data stored by the browser.
- **Cookies**: Extract cookies saved by websites.
- **Downloads**: Extract download history, including file names and URLs.
- **History**: Extract browsing history, including visited URLs, titles, and visit timestamps.

The data is saved in **CSV** or **JSON** formats, depending on the specific script. These scripts are helpful for users who wish to backup, analyze, or investigate their browser data.

## Supported Browsers
- **Google Chrome**
- **Brave**
- **Mozilla Firefox**
- **Microsoft Edge**

## Features
- **Cross-Platform Support**: Works on **Windows**, **macOS**, and **Linux**.
- **Comprehensive Data Extraction**: Extract multiple types of data from browsers, including bookmarks, passwords, history, cookies, downloads, and cache.
- **Easy-to-Use**: Scripts are simple to execute and require minimal setup.
- **CSV/JSON Output**: Data is saved in a readable format that can be analyzed using tools like Excel, Google Sheets, or custom Python scripts.

## Installation
To get started, follow these steps:

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Cr0mb/Browser-Data-Extraction-Scripts.git
   cd Browser-Data-Extraction-Scripts

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt

3. Ensure that you have the necessary permissions to access your browser data (e.g., reading from Chrome or Firefox profiles).

## Usage

Each type of data extraction has its own script. Here is an overview of how to use each:

1. Bookmarks Extraction
The bookmarks will be saved as bookmarks.json in the current directory.

2. Passwords Extraction
The passwords will be saved as passwords.json in the current directory.

3. Cache Extraction
The cache data will be saved as cache.json in the current directory.

4. Cookies Extraction
The cookies will be saved as cookies.json in the current directory.

5. Downloads Extraction
The download history will be saved as download_history.json in the current directory.

6. History Extraction
The history data will be saved as a CSV file for each browser, as well as a combined combined_history.csv.


## Output
The extracted data will be saved in various formats:

JSON (for bookmarks, passwords, cache, cookies, and downloads)

CSV (for history and combined history)

The data will be saved in the current working directory. You can specify a custom directory by modifying the script.


