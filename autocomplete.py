#!/usr/bin/env python3

def autocomplete(text, opts):
    comp_opts = [x for x in opts if x.startswith(text)]
    comp_opts.sort()
    return comp_opts[0] if comp_opts else False

if __name__ == '__main__':
    opts = ["foo", "bar", "baz"]
    print(autocomplete("f", opts))
    print(autocomplete("b", opts))
    print(autocomplete("baz", opts))
    print(autocomplete("s", opts))
