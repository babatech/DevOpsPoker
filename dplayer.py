#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
#  dodPoker:  a poker server to run automated texas hold'em
#  poker rounds with bots
#  Copyright (C) 2017 wobe-systems GmbH
# -----------------------------------------------------------
# -----------------------------------------------------------
# Configuration
# You need to change the setting according to your environment
gregister_url='http://192.168.8.100:5001'
glocalip_adr='192.168.8.104'

# -----------------------------------------------------------

from flask import Flask, request
from flask_restful import Resource, Api
import sys

from requests import put
import json

app = Flask(__name__)
api = Api(app)

# Web API to be called from the poker manager
class PokerPlayerAPI(Resource):

    ## return bid to caller
    #
    #  Depending on the cards passed to this function in the data parameter,
    #  this function has to return the next bid.
    #  The following rules are applied:
    #   -- fold --
    #   bid < min_bid
    #   bid > max_bid -> ** error **
    #   (bid > min_bid) and (bid < (min_bid+big_blind)) -> ** error **
    #
    #   -- check --
    #   (bid == 0) and (min_bid == 0) -> check
    #

    #

    #
    #   -- all in --
    #   bid == max_bid -> all in
    #
    #  @param data : a dictionary containing the following values - example: data['pot']
    #                min_bid   : minimum bid to return to stay in the game
    #                max_bid   : maximum possible bid
    #                big_blind : the current value of the big blind
    #                pot       : the total value of the current pot
    #                board     : a list of board cards on the table as string '<rank><suit>'
    #                hand      : a list of individual hand cards as string '<rank><suit>'
    #
    #                            <rank> : 23456789TJQKA
    #                            <suit> : 's' : spades
    #                                     'h' : hearts
    #                                     'd' : diamonds
    #                                     'c' : clubs
    #
    # @return a dictionary containing the following values
    #         bid  : a number between 0 and max_bid
    def __get_bid(self, data):
        #   -- call --
        #   (bid == min_bid) and (min_bid > 0)


        if data["hand"].count("A") >1 and data["board"].count("A") > 0:
            return data["max_bid"]

        if data["hand"].count("K") >1 and data["board"].count("K") > 0:
            return data["max_bid"]

        if data["hand"].count("Q") >1 and data["board"].count("Q") > 0:
            return data["max_bid"]

        if data["hand"].count("J") >1 and data["board"].count("J") > 0:
            return data["max_bid"]

        if data["hand"].count("T") >1 and data["board"].count("T") > 0:
            return data["max_bid"]

        if data["hand"].count("9") >1 and data["board"].count("9") > 0:
            return data["max_bid"]


        if data["hand"].count("8") >1 and data["board"].count("8") > 0:
            return data["max_bid"]

        if data["hand"].count("7") >1 and data["board"].count("7") > 0:
            return data["max_bid"]

        if data["hand"].count("6") >1 and data["board"].count("6") > 0:
            return data["max_bid"]

        if data["hand"].count("5") >1 and data["board"].count("5") > 0:
            return data["max_bid"]

        if data["hand"].count("4") >1  and data["board"].count("4") > 0:
            return data["max_bid"]

        if data["hand"].count("3") >1 and data["board"].count("3") > 0:
            return data["max_bid"]

        if data["hand"].count("2") >1 and data["board"].count("2") > 0:
            return data["max_bid"]

        r = []
        print(data)
        for c in data["hand"]:
            r.append(c[0])
        for c in data["board"]:
            r.append(c[0])
        seen = set()
        uniq = []
        dub = {}
        for x in r:
            if x not in seen:
                uniq.append(x)
                seen.add(x)
                dub[x] = 1

            else:
                dub[x] = dub[x] + 1
        if dub[x] > 2:
            return data["max_bid"]

        return data["min_bid"]







    # dispatch incoming get commands
    def get(self, command_id):

        data = request.form['data']
        data = json.loads(data)

        if command_id == 'get_bid':
            return {'bid': self.__get_bid(data)}
        else:
            return {}, 201

    # dispatch incoming put commands (if any)
    def put(self, command_id):
        return 201


api.add_resource(PokerPlayerAPI, '/dpoker/player/v1/<string:command_id>')

# main function
def main():

    # run the player bot with parameters
    if len(sys.argv) == 4:
        team_name = sys.argv[1]
        api_port = int(sys.argv[2])
        api_url = 'http://%s:%s' % (glocalip_adr, api_port)
        api_pass = sys.argv[3]
    else:
        print("""
DevOps Poker Bot - usage instruction
------------------------------------
python3 dplayer.py <team name> <port> <password>
example:
    python3 dplayer bazinga 40001 x407
        """)
        return 0


    # register player
    r = put("%s/dpoker/v1/enter_game"%gregister_url, data={'team': team_name, \
                                                           'url': api_url,\
                                                           'pass':api_pass}).json()
    if r != 201:
        raise Exception('registration failed: probably wrong team name or password')

    else:
        print('registration successful')

    try:
        app.run(host='0.0.0.0', port=api_port, debug=False)
    finally:
        put("%s/dpoker/v1/leave_game"%gregister_url, data={'team': team_name, \
                                                           'url': api_url,\
                                                           'pass': api_pass}).json()
# run the main function
if __name__ == '__main__':
    main()


