# System Design - JackPay

## TOC
- features of JackPay
- basic payments behavior
- objects

## Features of JackPay
- Application-layer payments network, single threaded
- Payers:
    - All entities on the app are the same: "payers"
        - these could be: corporations, individuals, political parties, software using our API, etc.
    - payers have ID info attached, and an account balance 
    - sends all payments to `Router` with target location
- Router:
    - central routing hub that connects payers, handles transfer of funds from `PayerA` to `PayerB`
    - updates ledger with payment action
    - has a list of network participants
        - this could likely be refactored out to a DB or what have you
    - logic for following features exist in here:
       - check balance payment sender to confirm available balance
       - confirm payment receiver is a known entity in 
       - transfer balance from payment sender to payment receiver
       - sends transaction to ledger for writing
       - related error handling
    - sees both sides of the payment interaction
- Ledger:
    - Object that writes to a CSV, which serves as the ledger
    - only records successful payments
    - the ledger istelf is a CSV
    - has the following data
        - DTG, sender, receiver, amount

## Basic Payments Behavior
- Example: successful payment
    - Sender actions:
        - `PayerA` wants to send to `PayerB`
        - `PayerA` calls `PayerA.sendPayment(PayerB, amount)`
        - `payer.sendPayment(xx, xx)` routes to `Router` parsing
    - Router actions:
        - Unpack payment object recv'd
        - Query `Router.fundsAvail(PayerA, amountRequested)`
        - Query `Router.receiverExists(PayerB, Payers)`
        - Test connect to `PayerB`
        - Send to `PayerB`
        - Confirm receipt
        - write to ledger `Router.writeToLedger(transcationData)
    - Ledger:
        - receive payment data
        - write to CSV file
        - notify Router of success/fail
    - Receiver
        - receive pamynet from `PayerA`
        - update acc balance
        - notify Router of completion

- Example: failed payment
    - Sender actions:
        - `PayerA` wants to send to `PayerB`
        - `PayerA` calls `PayerA.sendPayment(PayerB, amount)`
        - `payer.sendPayment(xx, xx)` routes to `Router` parsing
    - Router actions:
        - Unpack payment object recv'd
        - Query `Router.fundsAvail(PayerA, amountRequested)`
            - Fail, end TX, notify PayerA
        - Query `Router.receiverExists(PayerB, Payers)` 
            - Fail, end TX, notify PayerA
        - Send to `PayerB`
        - Confirm receipt
            - Fail, end TX, notify PayerA
    - Receiver
        - receive pamynet from `PayerA`
        - update acc balance
            - Fail, end TX, notify PayerA

- Example: Error handling locations and likely results
    - Sender actions:
        - `PayerA` wants to send to `PayerB`
        - `PayerA` calls `PayerA.sendPayment(PayerB, amount)`
        - `payer.sendPayment(xx, xx)` routes to `Router` parsing
            - Error handling, bad network connecton
    - Router actions:
        - Unpack payment object recv'd
        - Query `Router.fundsAvail(PayerA, amountRequested)`
            - Error handling, bad payment
        - Query `Router.receiverExists(PayerB, Payers)`
            - Error handling, bad dest
        - Test connect to `PayerB`
            - Error handling, bad network connecton
    - Router actions:
        - Send to `PayerB`
        - Confirm receipt
            - Error handling, bad network connecton
        - write to ledger `Router.writeToLedger(transcationData)
            - Error handling, bad network connecton
    - Ledger:
        - receive payment data
        - write to CSV file
            - Error handling, bad write
        - notify Router of success/fail
    - Receiver
        - receive pamynet from `PayerA`
            - Error handling, bad network connecton
        - update acc balance
            - Error handling, bad paymnet update, 
        - notify Router of completion
            - Error handling, bad network connection


## Objects
- `Class Payer`
    - `self.fields`
        - identifier (unique)
        - accountBalance 
            - TBD: how to make this writable only by Router, not object itself?
        - last TX time (possibly unique)
    - methods
        - `createPayment()`
            - creates payment packet to send
        - `sendPayment()`
            - sends payment to router
        - `testRouterLink()`
            - ping the router, confirm 200 ok
        - `queryBalance()`
            - get acc balance
        - `notifyFailure()`
            - multipurpose based on failure type, usually notifying router though
        - `updateBalance()`
            - TBD, this seems unwise, maybe make it a router function
- `Class Router`
    - `self.fields`
        - `activePayers`: 
            - list of payers active on the network
        - `currentSender`:
            - sender live for the current transaction
        - `currentRecv`
            - same
        - `ledgerData`
            - current connection info to reach ledger
    - methods
        - `confirmBalance()`
            - confirm sender has the balance
        - `sendPayment()`
            - send payment to recv
        - `pingLedger()`
            - confirm connection to ledger
        - `pingPayer()`
            - confirm connection to payer
        - `killPayment()`
            - error handling, kill payment for whatever reason

-- the big todo, how does a mixer fit into this, how to design such that it's easy to plug in





























