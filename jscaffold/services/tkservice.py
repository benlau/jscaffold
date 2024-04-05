from multiprocessing import Process, Pipe


def ask_tk_open_file():
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    root = Tk()
    root.attributes("-alpha", 0.01)
    root.attributes("-topmost", True)
    root.tk.eval(f"tk::PlaceWindow {root._w} center")
    root.withdraw()
    filename = askopenfilename()
    root.destroy()
    return filename


def worker(conn):
    try:
        filename = ask_tk_open_file()
        filename = filename if filename else ""
        conn.send({"filename": filename})
        conn.close()
    except Exception as e:
        conn.send({"error": str(e)})


def ask_open_file():
    parent_conn, child_conn = Pipe()
    p = Process(target=worker, args=(child_conn,))
    p.start()
    p.join()
    content = parent_conn.recv()
    if "error" in content:
        raise Exception(content["error"])
    return content["filename"]
