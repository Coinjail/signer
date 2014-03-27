#!/usr/bin/env python



from pybitcointools import *
import json
import argparse
import sys

#Signs each input of a raw transaction with the given private key
def signRawTransaction(rawtx, privateKey, redeemScript): 
    try:   
        txj = deserialize(rawtx)
        for i in range (0,len(txj['ins'])):
            sig =multisign(rawtx,i,redeemScript,privateKey)
            #print 'SIG:',sig
            rawtx = apply_multisignatures(rawtx,i,redeemScript,sig)
        return rawtx
    except Exception, e:
        print e
        return None

if __name__ == '__main__':

    signedTX = None
    if sys.stdin.isatty(): #terminal
        parser = argparse.ArgumentParser(description='Coinjail transaction signing tool. ( www.coinjail.com )')
        parser.add_argument("rawTX", help="The raw transaction string to be signed.")
        parser.add_argument("redeemScript", help="Redeemscript for multisig transactions.")
        parser.add_argument("privKey", help="Your private key.")

        args = parser.parse_args()
        signedTX = signRawTransaction(args.rawTX , args.privKey, args.redeemScript)
        if signedTX is not None:
            print signedTX
        else:
            print 'Error: Check arguments.'
    else: #pipe
        try:
            parser = argparse.ArgumentParser(description='Coinjail transaction signing tool. ( www.coinjail.com )')
            parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
            parser.add_argument("privKey", help="Your private key.")
            args = parser.parse_args()
            jsonString = args.infile.read()
            j = json.loads(jsonString)
            rawtx = j.get('rawTransaction', '')
            redeemScript = j.get('redeemScript','')
            signedTX = signRawTransaction(rawtx , args.privKey, redeemScript)
            j['signedTransaction'] = signedTX
            ret = json.dumps(j)
            print ret
        except Exception,e:
            print 'Error: Check arguments.' , e
    


