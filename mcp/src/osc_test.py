"""
OSC client for sending code to Sonic Pi via /run-code.

Usage:
    python osc_test.py
    python osc_test.py --ip 127.0.0.1 --port 4560 --code "sample :ambi_lunar_land"
"""

import argparse

from pythonosc import udp_client

default_code = """start_notes = ring(60, 62, 63, 62)
loop do
  my_chord = chord(start_notes.tick, :M7)
  play my_chord, release: 2
  16.times do
    play my_chord.choose
    sleep 0.125
  end
end
"""


def send_prophet_node(
    note: int = 70,
    velocity: int = 100,
    duration: int = 8,
    ip: str = "127.0.0.1",
    port: int = 4560,
):
    client = udp_client.SimpleUDPClient(ip, port)
    client.send_message("/trigger/prophet", [note, velocity, duration])
    print(f"Sent /trigger/prophet to {ip}:{port}")


def send_run_code(ip: str, port: int, code: str) -> None:
    client = udp_client.SimpleUDPClient(ip, port)
    workspace_id = 0
    client.send_message("/run-code", [workspace_id, code])
    print(f"Sent /run-code to {ip}:{port}")


def send_run_file():
    # sendosc localhost 4560 "/run-file" "/full/path/to/code.rb"
    abs_path = "/Users/nakanohiroki/mcp-sonic/mcp-sonic-pi/src/sample.rb"
    client = udp_client.SimpleUDPClient("127.0.0.1", 4560)
    client.send_message("/run-file", abs_path)
    print(f"Sent /run-file to 127.0.0.1:4560 with path {abs_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send Sonic Pi code via OSC /run-code")
    parser.add_argument("--ip", default="127.0.0.1", help="Sonic Pi OSC server IP")
    parser.add_argument(
        "--port", type=int, default=4560, help="Sonic Pi OSC server port"
    )
    parser.add_argument("--code", default=default_code, help="Sonic Pi code to run")
    args = parser.parse_args()

    send_run_code(args.ip, args.port, args.code)
    # send_prophet_node(ip=args.ip, port=args.port)
    # send_run_file()
