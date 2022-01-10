from django.shortcuts import redirect


def claim_voucher_view(request, voucher):
    print("Claiming voucher:", voucher)
    return redirect(f"/#{voucher}")
