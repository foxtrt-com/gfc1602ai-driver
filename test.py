from gfc1602ai import GFC1602AI

import board

lcd = GFC1602AI(
    rs=board.D7,
    rw=board.D8,
    e=board.D9,
    db0=board.D10,
    db1=board.D11,
    db2=board.D12,
    db3=board.D13,
    db4=board.D14,
    db5=board.D15,
    db6=board.D16,
    db7=board.D17
)

lcd.write_string("Hello, World!")
