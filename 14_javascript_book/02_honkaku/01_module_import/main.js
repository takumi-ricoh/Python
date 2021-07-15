'use strict';


import {Member, Area} from './lib/Util.mjs'

var mem = new Member('taro')
mem.self_intro()

var area = new Area('tokyo')
console.log(area.get_area())

