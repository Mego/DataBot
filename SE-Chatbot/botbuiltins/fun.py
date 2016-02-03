#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from Module import Command
import random
from . import upsidedown

module_name = "fun"

eyes = ['°', '゜', 'ಥ', "'", '•', '^', '⇀', 'ಠ', '๑']
mouths = ['□', 'Д', '益', 'ᴥ', '.', 'ʖ', 'ل͜', '³', 'ਊ']
arms = ['╯', 'ง', '┛', 'づ']


def exec_flip(cmd, bot, args, msg, event):
    if len(args) == 0:
        return 'Not enough arguments'
    left_eye = random.choice(eyes)
    right_eye = random.choice(eyes + [left_eye] * 20)
    mouth = random.choice(mouths)
    left_arm = random.choice(arms)
    right_arm = random.choice(arms + [left_arm] * 3)
    face = left_eye + mouth + right_eye

    flipped = upsidedown.transform(' '.join(args))

    return '(' + left_arm + face + ')' + right_arm + '︵' + flipped


def exec_doubleflip(cmd, bot, args, msg, event):
    if len(args) == 0:
        return 'Not enough arguments'
    inp = ' '.join(args)
    mirrored = ''.join(reversed(inp))
    mirrored_flipped = upsidedown.transform(mirrored)
    input_flipped = upsidedown.transform(inp)

    left_eye = random.choice(eyes)
    right_eye = random.choice(eyes + [left_eye] * 20)
    mouth = random.choice(mouths)
    face = left_eye + mouth + right_eye
    body = ' ︵ヽ(' + face + ')ﾉ︵ '

    return mirrored_flipped + ' ' + body + ' ' + input_flipped



commands = [
    Command('flip', exec_flip, 'This command will flip anything you throw at it. Syntax: `$PREFIXflip something`', False, False, None, None, None, None),
    Command('doubleflip', exec_doubleflip, 'This command will double-flip anything you throw at it. Syntax: `$PREFIXdoubleflip something`', False, False, None, None, None, None)
]
