from typing import Optional, Dict
from pathlib import Path
import shutil
import subprocess
import os

from rich import print, table
import typer
import tomlkit
from send2trash import send2trash


class BoardsApp:
    def __init__(
        self,
        board: str = "default",
        promote: str = "",
        demote: str = "",
        new: str = "",
        notes: str = "",
        remove: str = "",
        makeboard: str = "",
    ):
        self.user_config = self.get_user_config()
        try:
            self.board_dir = self.get_board_dir(board)
        except KeyError:
            print(f"[red]Board named {board} not found in config[/red]")
            return
        self.board_config = self.get_board_config()
        self.lanes = self.board_config["lanes"]
        if promote:
            self.move(promote, by=1)
        if demote:
            self.move(demote, by=-1)
        if new:
            self.new(new)
        if notes:
            self.edit(notes)
        if remove:
            self.remove(remove)
        if makeboard:
            self.make_board(makeboard)
        self.board = self.get_board()
        self.display_board()

    def get_board_dir(self, board: str, parent_board: str = "") -> Path:
        """
        Figure out the directory for a specific board

        board name found initialy through user config
        subboards can be found through board.subboard
        """
        boards: List[str] = board.split(".")
        if parent_board:
            lanes = self.get_board_config(parent_board)["lanes"]
            current_board: str = self.find_item(
                boards.pop(0),
                Path(parent_board),
                lanes=lanes,
            )
        else:
            current_board: str = self.user_config["boards"][boards.pop(0)]
        if len(boards) == 0:
            return Path(current_board)
        return self.get_board_dir(
            board=".".join(boards),
            parent_board=current_board,
        )

    def get_user_config(self):
        """
        Return user config
        """
        if os.name == "nt":
            home: str = os.environ["USERPROFILE"]
        else:
            home: str = os.environ["HOME"]
        config_path: Path = Path(home) / ".config" / "boards" / "config.toml"
        if config_path.exists():
            with open(config_path, "r") as file:
                contents = file.read()
            return tomlkit.loads(contents)
        print("No existing user config found, creating along with default board")
        default_board: Path = config_path.parent / "userboard"
        self.init_board(default_board)
        config = {
            "boards": {"default": str(default_board)},
            "editor": "vi",
        }
        with open(config_path, "w", encoding="utf-8") as file:
            file.write(tomlkit.dumps(config))
        print(
            f"[green]Config and board created at {config_path.parent}[/green]"
        )
        return config

    def get_board_config(self, board_dir: Optional[str] = None):
        """
        Return board configuration
        """
        board_dir = board_dir or self.board_dir
        with open(f"{board_dir}/board.toml", "r") as file:
            contents = file.read()
        board_config = tomlkit.loads(contents)
        return board_config

    def get_board(self) -> dict:
        """
        Return board
        """
        lanes = self.board_config["lanes"]
        board_dict = {k: [] for k in lanes}
        for lane in lanes:
            items = Path(f"{self.board_dir}/{lane}").glob("*")
            for item in items:
                board_dict[lane] += [item.stem]
        return board_dict

    def display_board(self) -> None:
        """
        Print board out as table
        """
        board_table: table.Table = table.Table()
        lanes: List[str] = self.board_config["lanes"]
        for lane in lanes:
            board_table.add_column(lane)
        board_length: int = max([len(i) for i in self.board.values()])
        display_board: Dict[str, str] = {
            k: v + ["" for i in range(board_length - len(v))]
            for k, v in self.board.items()
        }
        for i in range(board_length):
            board_table.add_row(*[display_board[k][i] for k in display_board])
        print(board_table)

    def move(self, item: str, by: int) -> None:
        """
        promote selected item to new location
        steps:
        1. find item
        2. move item
        """
        lane_dirs: List[Path] = [Path(i) for i in self.board_config["lanes"]]
        try:
            found: Path = self.find_item(item)
        except FileNotFoundError:
            print(f"[red]could not find '{item}' on board[/red]")
            return
        move_to_idx: int = self.lanes.index(found.parent.stem) + by
        if move_to_idx >= len(self.lanes) or move_to_idx < 0:
            print(f"[red]Cannot move '{item}' past '{found.parent.stem}'[red]")
            return
        move_to: Path = self.board_dir / lane_dirs[move_to_idx] / (found.stem + found.suffix)
        shutil.move(found, move_to)

    def new(self, item):
        """
        make new item on board at first lane
        """
        file: Path = self.board_dir / Path(self.lanes[0])
        with open(file / (item + ".md"), "w", encoding="utf-8") as file:
            file.write(f"# {item}\n(edit here to add notes)")

    def edit(self, item):
        """
        Edit item on board
        """
        try:
            found: Path = self.find_item(item)
        except FileNotFoundError:
            print(f"[red]Could not find '{item}' on board[/red]")
            return
        subprocess.run([self.user_config["editor"], found])

    def find_item(self, item, board_dir = None, lanes = None) -> Path:
        """
        Get item location
        Returns:
            item
        """
        board_dir = board_dir or self.board_dir
        lanes = lanes or self.lanes
        lane_dirs: List[Path] = [board_dir / Path(i) for i in lanes]
        for lane in lane_dirs:
            items: List[Path] = list(lane.iterdir())
            matches = [i for i in items if i.stem == item]
            if len(matches) > 0:
                return matches[0]
        raise FileNotFoundError()

    def remove(self, item):
        """
        Remove item from board
        """
        try:
            found: Path = self.find_item(item)
        except FileNotFoundError:
            print(f"[red]Could not find '{item}' on board[/red]")
            return
        move_to: Path = self.board_dir / Path(self.board_config["bin"]) / (found.stem + found.suffix)
        shutil.move(found, move_to)
        print(f"[green]'{item}' removed from board")

    def init_board(self, location: Path):
        """
        create board.toml, plus lanes
        """
        location.mkdir(parents=True)
        with open(location / "board.toml", "w", encoding="utf-8") as file:
            file.write('lanes = ["todo", "doing", "done"]\nbin = "archive"')
        for lane in ["todo", "doing", "done"]:
            (location / lane).mkdir()
        print(f"Board initialised as {location}")


    def make_board(self, item):
        """
        Get file, and replace with directory
        """
        try:
            found: Path = self.find_item(item)
        except FleNotFoundError:
            print(f"[red]Could not find '{item}' on board[/red]")
            return
        send2trash(found)
        self.init_board(found.parent / found.stem)
        
def run_app():
    typer.run(BoardsApp)
