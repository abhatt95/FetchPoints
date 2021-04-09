from constants import *

def _spend_points_(user_id,points):
    spending_per_payer = defaultdict(int)
    transactions_used = []
    copy_of_transactions = list(transactionOrderOf[user_id])
    for index,(time_stamp,payer,trans_points) in enumerate(transactionOrderOf[user_id]):
        transactions_used.append((time_stamp,payer,trans_points))    
        if trans_points > 0:
            max_points_can_be_deducted = trans_points
            current_sum = trans_points
            for f_t,f_pa,f_po in transactionOrderOf[user_id][index+1:]:
                if f_pa == payer:
                    current_sum += f_po
                    max_points_can_be_deducted = min(max_points_can_be_deducted,current_sum)

            if points > max_points_can_be_deducted:
                points -= max_points_can_be_deducted
                spending_per_payer[payer] -= max_points_can_be_deducted
            else:
                trans_points -= points
                spending_per_payer[payer] -= points
                points = 0
                transactionOrderOf[user_id][index] = (time_stamp,payer,trans_points)
            if points == 0:
                break        

    if points != 0:
        transactionOrderOf[user_id] = copy_of_transactions
        return None

    for used in transactions_used:
        if used in transactionOrderOf[user_id]:
            transactionOrderOf[user_id].remove(used)

    for k,v in spending_per_payer.items():
        balanceOf[user_id][k] += v

    return spending_per_payer

balanceOf = defaultdict()
# balanceOf = {
#  "user_id" : {
#    "payer1" : balance,
#    "payer2" : balance
#   }
# }
transactionOrderOf = defaultdict()
# transactionOrderOf = {
#  "user_id" : heapq([(unix_time_stamp1,payer1),(unix_time_stamp2,payer2),])
# }

update_balance_codes = {
    "TRANSACTION_SUCCESS" : "Transaction completed successfully.",
    "TRANSACTION_FAILED" : "Transaction failed."
}

def _update_balance(user_id,trans):
    key = trans.keys() 
    trans = json.loads(list(key)[0])
    print(" Transaction :",trans[PAYER],trans[POINTS],trans[TIMESTAMP])
    
    current_payer = trans[PAYER]
    current_points = trans[POINTS]
    current_time_stamp = datetime.datetime.strptime(trans[TIMESTAMP], '%Y-%m-%dT%H:%M:%SZ').timestamp()
    print("Time stamp :",current_time_stamp)
    if user_id not in balanceOf:
        balanceOf[user_id] = defaultdict(int)
    if current_payer not in balanceOf[user_id]:
        balanceOf[user_id][current_payer] = 0
    if balanceOf[user_id][current_payer] + current_points > 0:
        balanceOf[user_id][current_payer] += current_points
        if user_id not in transactionOrderOf:
            transactionOrderOf[user_id] = []
        transactionOrderOf[user_id].append((current_time_stamp,current_payer,current_points))
        transactionOrderOf[user_id].sort()

        return "TRANSACTION_SUCCESS"
    return "TRANSACTION_FAILED"
    
def _can_spend(user_id,points):
    rc = True
    total_points = 0
    for k,v in balanceOf[user_id].items():
        total_points += v
    if total_points >= points:
        return rc
    return not rc


