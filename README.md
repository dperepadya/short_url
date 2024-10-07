# FastAPI URL Shortener

This project is a URL shortener built with FastAPI, featuring a choice between storing URLs in a JSON file or a MongoDB database.
Users can input a long URL and receive a shortened version, which can later be used to access the original URL.

## Features

- Shorten long URLs and store them in either a JSON file or MongoDB.
- Redirect users from shortened URLs to the original URLs.
- Validate user input to ensure that the provided URLs are valid.
- Track how many times a shortened URL has been accessed.

## Technologies Used

- **FastAPI**: A modern web framework for building APIs with Python.
- **aiofiles**: For asynchronous file handling.
- **Motor**: An async driver for MongoDB.
- **Pydantic**: For data validation and settings management.
- **Validators**: For URL validation.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- MongoDB (if you choose to use the MongoDB storage option)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dperepadya/short_url.git
   
