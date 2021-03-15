from rawnicorn.cmdline import cmdline_parser
from rawnicorn.config import bind_config
from rawnicorn.master import MasterRawnicorn

if __name__ == "__main__":
    # cfg
    cmdline_args = cmdline_parser.parse_args()
    cfg = bind_config(
        cmdline_args.host, cmdline_args.port, cmdline_args.workers, cmdline_args.threads, cmdline_args.log_level
    )

    # booting
    server = MasterRawnicorn(cfg)
    server.boot()
