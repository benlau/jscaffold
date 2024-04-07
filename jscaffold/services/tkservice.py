from multiprocessing import Process, Pipe

from jscaffold.iounit.format import FileType


def ask_tk_open_file_dialog(file_type: FileType = FileType.File):
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename, askdirectory

    root = Tk()
    root.attributes("-alpha", 0.01)
    root.attributes("-topmost", True)
    root.tk.eval(f"tk::PlaceWindow {root._w} center")
    root.withdraw()

    if file_type == FileType.Directory.value:
        path = askdirectory()
    else:
        path = askopenfilename()
    root.destroy()
    return path


def worker(conn, file_type: FileType = FileType.File):
    try:
        path = ask_tk_open_file_dialog(file_type)
        path = path if path else ""
        conn.send({"path": path})
        conn.close()
    except Exception as e:
        conn.send({"error": str(e)})


class TKService:
    def open_file_dialog(file_type: FileType = FileType.File):
        parent_conn, child_conn = Pipe()
        p = Process(target=worker, args=(child_conn, file_type))
        p.start()
        p.join()
        content = parent_conn.recv()
        if "error" in content:
            raise Exception(content["error"])
        return content["path"]


tk_serivce = TKService
