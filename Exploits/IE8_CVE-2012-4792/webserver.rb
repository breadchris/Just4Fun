#!/usr/bin/ruby
#require 'rubygems'
require 'webrick'

log = WEBrick::Log.new
log.level = WEBrick::Log::DEBUG if $DEBUG
serv = WEBrick::HTTPServer.new({:Port => 8000, :Logger => log})
serv.mount("/", WEBrick::HTTPServlet::FileHandler, Dir.pwd)
trap(:INT){ serv.shutdown }
serv.start
