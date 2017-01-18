def branch(frame, offset):
    next_pc = frame.thread.pc + offset
    frame.set_next_pc(next_pc)
