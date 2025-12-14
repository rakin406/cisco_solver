<h2 align="center">CISCO Solver</h3>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

This program looks at the screen of your browser and scans the questions. It then searches the questions online and finds the relevant answers. The program automatically gives input (clicking, typing etc.) through the use of keyboard and mouse automation.

The program has a few bugs as it is only a prototype. It cannot solve matching questions. The program has an accuracy of approximately 90%, thus I highly suggest you to review the answers from the website <https://itexamanswers.net/>.

<!-- GETTING STARTED -->

## Getting Started

Follow these steps to use this program.

### Prerequisites

This is a list of things you need to use the program.

- Python

### Installation

1. Go to the top of this repository and click on the "<> Code" button.
2. Download the ZIP file.
3. Extract the ZIP file to a known place.
4. Open the folder using your file explorer, VSCode or any code editor.
5. If using file explorer, right click inside the folder and click on
   "Open in Terminal". If using VSCode, click on "Terminal" at the top
   and create a new terminal.
6. Run these commands inside the terminal.
   ```sh
   pip install -r requirements.txt
   ```

<!-- USAGE EXAMPLES -->

## Usage

Open your browser and go to netacad website. Then open your module exam and click on
"start". Close all other windows except the browser and terminal. Run this command in the terminal back in VSCode or Command Prompt.

```sh
python solver.py
```

Make sure not to move your mouse or press any keys. Now, sit back and relax!

Just kidding! You still have to make sure that the program is running correctly.
It will sometimes stop, and in that case you have to solve that specific question
yourself and then restart the program. The program might make 1/2 mistakes so
please check the answers online.

If in any case you want to stop the program, simply move the mouse to a corner of
the screen or press Ctrl-C in the terminal.

<!-- ROADMAP -->

## Roadmap

- [✅] Add support for checkpoint exams
- [ ] Make a portable executable

<!-- CONTACT -->

## Contact

Rakin Rahman - [@instagram_handle](https://www.instagram.com/rakin_406/) - rakinrahman406@gmail.com
