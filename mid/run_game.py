"""簡易啟動器：在本機啟動靜態 HTTP Server 並開啟 minesweeper.html

用法:
  python run_game.py          # 開啟 http://127.0.0.1:8000/minesweeper.html
  python run_game.py --port 9000
  python run_game.py --no-browser
"""
import os
import argparse
import webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler


def serve(port: int, open_browser: bool):
    # Try to run the Flask app from game_logic if available
    base_dir = os.path.dirname(__file__)
    os.chdir(base_dir)
    try:
        from game_logic import app
        url = f'http://127.0.0.1:{port}/minesweeper.html'
        print(f"Starting Flask app at {url}")
        if open_browser:
            try:
                webbrowser.open(url)
            except Exception as e:
                print(f"無法自動開啟瀏覽器: {e}")
        # note: use app.run rather than server.serve_forever
        app.run(host='127.0.0.1', port=port)
    except Exception as e:
        print('Flask not available or failed to start:', e)
        print('Falling back to a simple static HTTP server. To use Flask backend, install Flask and try again: pip install flask')
        server = ThreadingHTTPServer(('127.0.0.1', port), SimpleHTTPRequestHandler)
        url = f'http://127.0.0.1:{port}/minesweeper.html'
        print(f"Serving {base_dir} at {url}")

        if open_browser:
            try:
                webbrowser.open(url)
            except Exception as e:
                print(f"無法自動開啟瀏覽器: {e}")

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n收到中斷，正在關閉伺服器...")
        finally:
            server.shutdown()
            server.server_close()
            print("伺服器已關閉")


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='啟動本機伺服器並開啟 Minesweeper 網頁（會優先使用 Flask）')
    p.add_argument('--port', '-p', type=int, default=8000, help='伺服器連接埠，預設 8000')
    p.add_argument('--no-browser', dest='open_browser', action='store_false', help='不要自動開啟預設瀏覽器')
    args = p.parse_args()

    serve(args.port, args.open_browser) 
