# Project related to Course Subject: Information Retrieval.

## Making this Simple Infomation Retrival System for aesopa10.txt file. 


# Simple Information Retrieval System

## Project Description

This project is a simple information retrieval system that allows users to search for documents based on keywords. The system uses a vector space model to represent documents as vectors and calculate the cosine similarity between the query vector and document vectors. The system also uses a simple inverted index to speed up the search process and simple linear search model as control. 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

<!--
- [Issues](#issues)
- [Changelog](#changelog)
- [Roadmap](#roadmap)
- [Support](#support)
- [License](#license)
-->
## Installation

This project does not demand any additional libraries in python. The only thing you need to do is to clone the repository and run the simple_information_retrival.py file as the usage specifies the command line arguments. 

## Usage

The system can be run from the command line using the following command to list a few:

```bash 
- python simple_information_retrival.py --extract-collection aesopa10.txt
- python simple_information_retrival.py --query "somesearchterm" --model "vector/bool" --search-mode "inverted/linear" --documents "original/no_stopwords" --stemming
- python simple_information_retrival.py --query "somesearchterm" --model "vector/bool" --search-mode "inverted/linear" --documents "original/no_stopwords"
python simple_information_retrival.py --query "somesearchterm" --model "vector" --documents "original/no_stopwords"

```

## Issues

If your repository uses GitHub's issue tracking system, provide guidelines on how to report issues, how to submit feature requests, and how to contribute to issue discussions.

<!-->
## Changelog

Include a changelog or release notes detailing the project's version history, changes, and updates.

## Roadmap

If applicable, outline the future development plans for the project, including upcoming features and enhancements.

## Support

Provide details on how users can get support or assistance with using the project. Include contact information or links to communication channels (e.g., Discord, Gitter, Stack Overflow, etc.).

## License

Specify the project's license information, including the license type and any relevant copyright or authorship details.

-->