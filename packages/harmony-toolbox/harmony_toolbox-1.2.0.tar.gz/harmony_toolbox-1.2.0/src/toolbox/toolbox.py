import os, requests, time, json, subprocess
from pytimedinput import timedInteger
from subprocess import Popen, PIPE, run
from ast import literal_eval
from toolbox.config import EnvironmentVariables
from os import environ
from datetime import datetime
from colorama import Fore, Back, Style
from pyhmy import blockchain, transaction
from requests.exceptions import HTTPError
from toolbox.library import (
    process_command,
    print_stars,
    print_stars,
    print_whitespace,
    ask_yes_no,
    return_txt,
    find_port,
    install_hmy,
    get_sign_pct,
    load_var_file,
    get_wallet_balance,
    get_rewards_balance,
    string_stars,
    set_var,
    free_space_check,
    server_drive_check,
    all_sys_info,
    coming_soon,
    get_vote_choice,
    get_validator_wallet_name,
    governance_member_voting,
    proposal_choices_option,
    menu_ubuntu_updates,
    menu_reboot_server,
    finish_node,
    pull_harmony_update,
    version_checks,
    harmony_service_status,
    get_folders,
    validator_stats_output,
    get_db_size,
    first_setup,
    update_text_file,
    get_shard_menu,
    set_main_or_test,
    recover_wallet,
    refreshing_stats_message,
    passphrase_status,
)


def parse_flags(parser):
    config = EnvironmentVariables()
    print_stars()
    # Add the arguments
    parser.add_argument(
        "-s",
        "--stats",
        action="store_true",
        help="Run your stats if Harmony is installed and running.",
    )

    parser.add_argument(
        "-u",
        "--upgrade",
        action="store_true",
        help="Upgrade your Harmony binary if an upgrade is available.",
    )

    parser.add_argument(
        "-c",
        "--collect",
        action="store_true",
        help="Collect your rewards to your validator wallet",
    )

    parser.add_argument(
        "-cs",
        "--collect-send",
        action="store_true",
        help="Collect your rewards to your validator wallet and send them to your rewards wallet",
    )

    parser.add_argument(
        "-i",
        "--install",
        action="store_true",
        help="Install Harmony ONE and hmy CLI if not installed.",
    )

    args = parser.parse_args()

    print(Fore.RESET)

    if args.install:
        first_setup()

    if args.upgrade:
        update_harmony_app()

    if args.stats:
        run_multistats()
        finish_node()

    if args.collect:
        rewards_collector(config.working_rpc_endpoint)
        finish_node()

    if args.collect_send:
        rewards_collector(config.working_rpc_endpoint, True)
        finish_node()


def run_multistats():
    refreshing_stats_message()
    folders = get_folders()
    validator_stats_output(folders)
    return


def collect_rewards(pending_rewards_balance, networkCall=EnvironmentVariables.hmy_app):
    print(f"*\n* Collecting {pending_rewards_balance} $ONE Rewards, awaiting confirmation...\n")
    command = f"{networkCall} staking collect-rewards --delegator-addr {environ.get('VALIDATOR_WALLET')} --gas-price 100 {environ.get('PASS_SWITCH')}"
    result = process_command(command, True, False)
    if result:
        print("*\n*\n* Rewards collection Finished.\n")
    else:
        print("*\n*\n* Rewards collection Failed.\n")


def send_rewards(networkCall, sendAmount, rewards_wallet):
    command = f"{networkCall} transfer --amount {sendAmount} --from {environ.get('VALIDATOR_WALLET')} --from-shard 0 --to {rewards_wallet} --to-shard 0 --gas-price 100 {environ.get('PASS_SWITCH')}"
    result = process_command(command, True, False)
    if result:
        print("*\n*\n* Rewards sending Finished.\n")
    else:
        print("*\n*\n* Rewards sending Failed.\n")


def send_rewards_func(suggested_send, validator_wallet_balance, rewards_wallet, validator_wallet, bypass=False):
    if bypass == False:
        print("*\n*\n")
        print_stars()
        print("\n* Send your Harmony ONE Rewards?")
        print_stars()
        question = ask_yes_no(
            f"* You have {validator_wallet_balance} $ONE available to send. We suggest sending {suggested_send} $ONE using your reservation settings.\n* Would you like to send {suggested_send} $ONE to {rewards_wallet} now? (YES/NO)"
        )
        if question == False:
            print("*\n*\n* Skipping sending of rewards.\n")
            return
    print(f"*\n*\n* Sending {suggested_send} $ONE Rewards to {rewards_wallet}, awaiting confirmation...\n")
    send_rewards(EnvironmentVariables.hmy_app, suggested_send, rewards_wallet)
    validator_wallet_balance = get_wallet_balance(validator_wallet)
    rewards_wallet_balance = get_wallet_balance(rewards_wallet)
    print(f"*\n*\n* Current Validator Wallet Balance: {validator_wallet_balance} $ONE\n*")
    print(f"*\n*\n* Current Rewards Wallet Balance: {rewards_wallet_balance} $ONE\n*\n*")
    return


def rewards_sender(
    rewards_wallet=environ.get("REWARDS_WALLET"),
    validator_wallet=environ.get("VALIDATOR_WALLET"),
) -> None:
    validator_wallet_balance = get_wallet_balance(validator_wallet)
    suggested_send = validator_wallet_balance - int(environ.get("GAS_RESERVE"))
    if suggested_send >= 1:
        send_rewards_func(suggested_send, validator_wallet_balance, rewards_wallet, validator_wallet)
    else:
        print("*\n* Wallet balance is less than your gas reservation, please try again later.\n*\n")
    validator_wallet_balance = get_wallet_balance(validator_wallet)
    rewards_wallet_balance = get_wallet_balance(rewards_wallet)
    print(
        f"*\n*\n* Current Validator Wallet Balance: {validator_wallet_balance} $ONE\n*\n* Current Rewards Wallet Balance: {rewards_wallet_balance}\n*\n*"
    )
    return


def rewards_collector(
    rpc,
    bypass=False,
    rewards_wallet=environ.get("REWARDS_WALLET"),
    validator_wallet=environ.get("VALIDATOR_WALLET"),
) -> None:
    pending_rewards_balance = get_rewards_balance(rpc, validator_wallet)
    print_stars()
    print("* Harmony ONE Rewards Collection")
    print_stars()
    if bypass == False:
        question = ask_yes_no(
            f"*\n* For your validator wallet {validator_wallet}\n* You have {pending_rewards_balance} $ONE pending.\n* Would you like to collect your rewards on the Harmony mainnet? (YES/NO) "
        )
        if question:
            bypass = True
        else:
            print("*\n*\n* Skipping collection of rewards.\n")
    if bypass == True:
        collect_rewards(pending_rewards_balance)
        print_stars()
        print(
            Fore.GREEN + f"* mainnet rewards for {validator_wallet} have been collected." + Style.RESET_ALL + Fore.GREEN
        )
        print_stars()
    validator_wallet_balance = get_wallet_balance(validator_wallet)
    suggested_send = validator_wallet_balance - int(environ.get("GAS_RESERVE"))
    if suggested_send >= 1:
        send_rewards_func(suggested_send, validator_wallet_balance, rewards_wallet, validator_wallet, bypass)
    else:
        validator_wallet_balance = get_wallet_balance(validator_wallet)
        rewards_wallet_balance = get_wallet_balance(rewards_wallet)
        print(f"*\n*\n* Balance too low to send to rewards wallet\n")
        print(f"*\n*\n* Current Validator Wallet Balance: {validator_wallet_balance} $ONE\n*")
        print(f"* Current Rewards Wallet Balance: {rewards_wallet_balance} $ONE\n*\n*")
    return


def menu_topper_regular(software_versions) -> None:
    config = EnvironmentVariables()
    # Get stats & balances
    try:
        load_1, load_5, load_15 = os.getloadavg()
        sign_percentage = get_sign_pct()
        total_balance = get_wallet_balance(environ.get("VALIDATOR_WALLET"))
        remote_data_shard_0, local_data_shard, remote_data_shard = menu_validator_stats()
    except (ValueError, KeyError, TypeError) as e:
        print(f"* Error fetching data: {e}")
    # Print Menu
    print_stars()
    print(
        f'{Fore.GREEN}* Validator Toolbox for {Fore.CYAN}Harmony ONE{Fore.GREEN} Validators by Easy Node   v{environ.get("EASY_VERSION")}{Fore.WHITE}   https://easynode.pro {Fore.GREEN}*'
    )
    print_stars()
    print(
        f'* Your validator wallet address is: {Fore.RED}{str(environ.get("VALIDATOR_WALLET"))}{Fore.GREEN}\n* Your $ONE balance is:             {Fore.CYAN}{str(round(total_balance, 2))}{Fore.GREEN}\n* Your pending $ONE rewards are:    {Fore.CYAN}{str(round(get_rewards_balance(config.working_rpc_endpoint, environ.get("VALIDATOR_WALLET")), 2))}{Fore.GREEN}\n* Server Hostname & IP:             {Fore.BLUE}{EnvironmentVariables.server_host_name}{Fore.GREEN} - {Fore.YELLOW}{EnvironmentVariables.external_ip}{Fore.GREEN}'
    )
    harmony_service_status(environ.get("SERVICE_NAME", "harmony"))
    print(
        f'* Epoch Signing Percentage:         {Style.BRIGHT}{Fore.GREEN}{Back.BLUE}{sign_percentage} %{Style.RESET_ALL}{Fore.GREEN}\n* Current disk space free: {Fore.CYAN}{free_space_check(os.environ.get("HARMONY_DIR")): >6}{Fore.GREEN}\n* Current harmony version: {Fore.YELLOW}{software_versions["harmony_version"]}{Fore.GREEN}, has upgrade available: {software_versions["harmony_upgrade"]}\n* Current hmy version: {Fore.YELLOW}{software_versions["hmy_version"]}{Fore.GREEN}, has upgrade available: {software_versions["hmy_upgrade"]}'
    )
    print_stars()
    if environ.get("SHARD") != "0":
        print(
            f"* Note: Running on shard {environ.get('SHARD')}, Shard 0 is no longer needed locally and should be under 300MB\n* Remote Shard 0 Epoch: {remote_data_shard_0['result']['shard-chain-header']['epoch']}, Current Block: {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}, Local Shard 0 Size: {get_db_size(os.environ.get('HARMONY_DIR'), '0')}"
        )
        print(
            f"* Remote Shard {environ.get('SHARD')} Epoch: {remote_data_shard['result']['shard-chain-header']['epoch']}, Current Block: {literal_eval(remote_data_shard['result']['shard-chain-header']['number'])}"
        )
        print(
            f"*  Local Shard {environ.get('SHARD')} Epoch: {local_data_shard['result']['shard-chain-header']['epoch']}, Current Block: {literal_eval(local_data_shard['result']['shard-chain-header']['number'])}, Local Shard {environ.get('SHARD')} Size: {get_db_size(os.environ.get('HARMONY_DIR'), environ.get('SHARD'))}"
        )
    if environ.get("SHARD") == "0":
        print(
            f"* Remote Shard {environ.get('SHARD')} Epoch: {remote_data_shard_0['result']['shard-chain-header']['epoch']}, Current Block: {literal_eval(remote_data_shard_0['result']['shard-chain-header']['number'])}"
        )
        print(
            f"*  Local Shard {environ.get('SHARD')} Epoch: {local_data_shard['result']['shard-chain-header']['epoch']}, Current Block: {literal_eval(local_data_shard['result']['shard-chain-header']['number'])}"
        )
    print(
        f"* CPU Load Averages: {round(load_1, 2)} over 1 min, {round(load_5, 2)} over 5 min, {round(load_15, 2)} over 15 min"
    )
    print_stars()


def menu_regular(software_versions) -> None:
    menu_topper_regular(software_versions)
    for x in return_txt(EnvironmentVariables.main_menu_regular):
        x = x.strip()
        try:
            x = eval(x)
        except SyntaxError:
            pass
        if x:
            print(x)


def get_wallet_json(wallet: str) -> str:
    test_or_main = environ.get("NETWORK")
    try:
        response = requests.get(f"https://api.stake.hmny.io/networks/{test_or_main}/validators/{wallet}")
        response.raise_for_status()
        # access JSOn content
        json_response = response.json()
    #        print("Entire JSON response")
    #        print(json_response)
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(
            f'* You have not created your validator yet, try again after you add one!\n* cd ~/harmony\n* ./hmy keys recover-from-mnemonic {EnvironmentVariables.active_user} {environ.get("PASS_SWITCH")}'
        )
        input("Press ENTER to return to the main menu.")
        return
    except Exception as err:
        print(f"Other error occurred: {err}")
        input("Press ENTER to return to the main menu.")
        return
    return json_response


def tmi_server_info() -> None:
    validator_wallet = environ.get("VALIDATOR_WALLET")
    json_response = get_wallet_json(validator_wallet)
    for key, value in json_response.items():
        print(key, ":", value)
    print_stars()
    input("Press ENTER to return to the main menu.")


def set_rewards_wallet() -> None:
    rewards_wallet = environ.get("REWARDS_WALLET")
    gas_reserve = environ.get("GAS_RESERVE")
    if rewards_wallet is None:
        question = ask_yes_no("* Would you like to add an address to send your rewards too? (YES/NO)")
        if question:
            rewards_wallet = input(f"* Input your one1 address to send rewards into, please input your address now: ")
            if rewards_wallet.startswith("one1"):
                set_var(EnvironmentVariables.dotenv_file, "REWARDS_WALLET", rewards_wallet)
            else:
                print("* Wallet does not start with one1, please try again.")
                return
        return
    else:
        question = ask_yes_no(
            f"* Your current saved rewards wallet address is {rewards_wallet}\n* Would you like to update the address you send your rewards too? (YES/NO)"
        )
        if question:
            rewards_wallet = input(f"* Input your one1 address to send rewards into, please input your address now: ")
            if rewards_wallet.startswith("one1"):
                set_var(EnvironmentVariables.dotenv_file, "REWARDS_WALLET", rewards_wallet)
            else:
                print("* Wallet does not start with one1, please try again.")
                return
            set_gas_reserve()
            return
        else:
            question = ask_yes_no(
                f"* Your current wallet gas reservation is {gas_reserve} $ONE\n* Would you like to update your reservation total? (YES/NO)"
            )
            if question:
                set_gas_reserve()
                return
    return


def set_gas_reserve() -> None:
    gas_reserve = environ.get("GAS_RESERVE")
    question = ask_yes_no(
        f"* Your current total of $ONE to reserve for fees is {gas_reserve}\n* Would you like to update the reserve total? (YES/NO)"
    )
    if question:
        ask_reserve_total()
    return


def ask_reserve_total() -> None:
    reserve_total = input("* How much $ONE would you like to keep reserved for fees? ")
    set_reserve_total(reserve_total)
    return


def set_reserve_total(reserve_total):
    set_var(EnvironmentVariables.dotenv_file, "GAS_RESERVE", reserve_total)


def drive_check() -> None:
    server_drive_check(EnvironmentVariables.dotenv_file, os.environ.get("HARMONY_DIR"))
    return


def run_check_balance() -> None:
    config = EnvironmentVariables()
    menu_check_balance(config.working_rpc_endpoint, environ.get("VALIDATOR_WALLET"))


def bingo_checker():
    command = f"grep BINGO {os.environ.get('HARMONY_DIR')}/latest/zerolog-harmony.log | tail -10"
    process_command(command, shell=True, print_output=True)
    print_stars()
    print("* Press enter to return to the main menu.")
    print_stars()
    input()


def run_rewards_collector() -> None:
    config = EnvironmentVariables()
    rewards_collector(config.working_rpc_endpoint)
    return


def safety_defaults() -> None:
    # default settings section
    set_var(EnvironmentVariables.dotenv_file, "EASY_VERSION", EnvironmentVariables.easy_version)
    if environ.get("GAS_RESERVE") is None:
        set_var(EnvironmentVariables.dotenv_file, "GAS_RESERVE", "5")
    if environ.get("REFRESH_TIME") is None:
        set_var(EnvironmentVariables.dotenv_file, "REFRESH_TIME", "30")
    if environ.get("REFRESH_OPTION") is None:
        set_var(EnvironmentVariables.dotenv_file, "REFRESH_OPTION", "True")
    if environ.get("HARMONY_DIR") is None:
        if os.path.isdir(f"{EnvironmentVariables.user_home_dir}/harmony"):
            set_var(EnvironmentVariables.dotenv_file, "HARMONY_DIR", f"{EnvironmentVariables.user_home_dir}/harmony")
            return
        elif os.path.isfile(f"{EnvironmentVariables.user_home_dir}/harmony"):
            try:
                subprocess.run(f"{EnvironmentVariables.user_home_dir}/harmony -V", check=True)
                set_var(EnvironmentVariables.dotenv_file, "HARMONY_DIR", f"{EnvironmentVariables.user_home_dir}")
                return
            except subprocess.CalledProcessError as e:
                print(
                    "* Well this is odd, somehow harmony was not found.\n*\n* You can add the HARMONY_DIR variable to your ~/.easynode.env file\n* Example default location: HARMONY_DIR = /home/serviceharmony/harmony\n*\n* Or contact Easy Node for custom configuration help."
                )
                raise SystemExit(0)
        else:
            first_setup()
    # always set conf to 13 keys, shard max
    if os.path.exists(EnvironmentVariables.harmony_conf):
        update_text_file(EnvironmentVariables.harmony_conf, "MaxKeys = 10", "MaxKeys = 13")
    if os.path.isfile(f"{os.environ.get('HARMONY_DIR')}/blskey.pass"):
        update_text_file(EnvironmentVariables.harmony_conf, 'PassFile = ""', f'PassFile = "blskey.pass"')
    passphrase_status()
    get_shard_menu()
    set_main_or_test()
    if environ.get("VALIDATOR_WALLET") is None:
        # Recover wallet or have them add address
        recover_wallet()


def refresh_toggle() -> None:
    if environ.get("REFRESH_OPTION") == "True":
        answer = ask_yes_no(f"* Refresh is currently enabled. Would you like to disable it? (Y/N) ")
        if answer:
            set_var(EnvironmentVariables.dotenv_file, "REFRESH_OPTION", "False")
        else:
            answer = ask_yes_no(
                f'* Your current refresh time is {str(environ.get("REFRESH_TIME"))} seconds. Would you like to change the delay? (Y/N) '
            )
            if answer:
                delay_time = timedInteger(
                    "* Enter the number of seconds to wait before auto-refreshing: ",
                    timeout=-1,
                    resetOnInput=True,
                    allowNegative=False,
                )
                set_var(EnvironmentVariables.dotenv_file, "REFRESH_TIME", str(delay_time[0]))
    else:
        answer = ask_yes_no(f"* Refresh is currently disabled. Would you like to enable it? (Y/N) ")
        if answer:
            set_var(EnvironmentVariables.dotenv_file, "REFRESH_OPTION", "True")
        answer = ask_yes_no(
            f'* Your current refresh time is {str(environ.get("REFRESH_TIME"))} seconds. Would you like to change the delay? (Y/N) '
        )
        if answer:
            delay_time = timedInteger(
                "* Enter the number of seconds to wait before auto-refreshing: ",
                timeout=-1,
                resetOnInput=True,
                allowNegative=False,
            )
            set_var(EnvironmentVariables.dotenv_file, "REFRESH_TIME", str(delay_time[0]))
    load_var_file(EnvironmentVariables.dotenv_file)
    return


def update_stats_option() -> None:
    if environ.get("REFRESH_OPTION") == "True":
        print(
            f"*  20 - Disable auto-update       - Disable Refresh or Change Delay Timer: {str(environ.get('REFRESH_TIME'))} seconds"
        )
    else:
        print(f"*  20 - Enable Auto update        - Enable Update Timer")


def harmony_voting() -> None:
    print_stars()
    print("* Harmony Voting")
    print_stars()
    question, proposal = proposal_choices_option()
    if proposal == "Quit" or question == False:
        return
    validator_wallet_name = get_validator_wallet_name(environ.get("VALIDATOR_WALLET"))
    if proposal == "HIP-30v2":
        vote_choice_option, vote_choice_text = get_vote_choice()
        if vote_choice_text == "Quit":
            return
        print(
            f"* Voting for {vote_choice_option} - {vote_choice_text} on proposal {proposal}\n* Please enter your validator wallet password now: \n"
        )
        command = f"{environ.get('HARMONY_DIR')}/hmy governance vote-proposal --space harmony-mainnet.eth --proposal 0xce5f516c683170e4164a06e42dcd487681f46f42606b639955eb7c0fa3b13b96 --proposal-type single-choice --choice {vote_choice_option} --key {validator_wallet_name} --passphrase"
        process_command(
            command,
            True,
            True,
        )
    if proposal == "Governance for Harmony Recovery Wallet":
        vote_choice_option, vote_choice_names_list = governance_member_voting()
        vote_choice_names = "\n* ".join(
            vote_choice_names_list[1:-1].split(", ")
        )  # Extracting the names and formatting them
        question = ask_yes_no(
            f"* You have selected\n*\n* {vote_choice_names}\n*\n* Are you sure you want to vote for this list?  (Yes/No) "
        )
        if question:
            print(
                f"* Voting for {vote_choice_option} - {vote_choice_names_list} on proposal {proposal}\n* Please enter your validator wallet password now: \n"
            )
            command = f"{environ.get('HARMONY_DIR')}/hmy governance vote-proposal --space harmony-mainnet.eth --proposal 0x80b87627254aa71870407a3c95742aa30c0e5ccdc81da23a1a54dcf0108778ae --proposal-type approval --choice \"{vote_choice_option}\" --key {validator_wallet_name} --passphrase"
            process_command(
                command,
                True,
                True,
            )
        else:
            print("*\n* Returning to menu...")

    return


def start_regular_node() -> None:
    # Check online versions of harmony & hmy and compare to our local copy.
    refreshing_stats_message()
    software_versions = version_checks(environ.get("HARMONY_DIR"))
    run_regular_node(software_versions)


def run_regular_node(software_versions) -> None:
    menu_options = {
        0: finish_node,
        1: refreshing_stats_message,
        2: menu_active_bls,
        3: bingo_checker,
        4: run_rewards_collector,
        5: rewards_sender,
        6: set_rewards_wallet,
        7: harmony_voting,
        8: menu_service_stop_start,
        9: menu_service_restart,
        10: harmony_binary_upgrade,
        11: hmy_cli_upgrade,
        12: menu_ubuntu_updates,
        13: drive_check,
        14: tmi_server_info,
        15: all_sys_info,
        20: refresh_toggle,
        999: menu_reboot_server,
    }
    while True:
        load_var_file(EnvironmentVariables.dotenv_file)
        menu_regular(software_versions)
        if software_versions["harmony_upgrade"] == "True":
            print(
                f'* The harmony binary has an update available to version {software_versions["online_harmony_version"]}\n* Option #10 will upgrade you, but you may miss a block while it upgrades & restarts.\n* Currently installed version {software_versions["harmony_version"]}'
            )
            print_stars()
        if software_versions["hmy_upgrade"] == "True":
            print(
                f'* The hmy binary has an update available to version {software_versions["online_hmy_version"]}\n* Option #11 will upgrade you.\n* Currently installed version {software_versions["hmy_version"]}'
            )
            print_stars()
        if environ.get("REFRESH_OPTION") == "True":
            try:
                # run timed input
                option, timedOut = timedInteger(
                    f"* Auto refresh enabled, Enter your menu choice: ",
                    timeout=int(environ.get("REFRESH_TIME")),
                    resetOnInput=True,
                    allowNegative=False,
                )
                if timedOut:
                    start_regular_node()
                else:
                    print_stars()
                    menu_options[option]()
                    if option != 1:
                        start_regular_node()
            except KeyError:
                print(f"* Bad option, try again. Press enter to continue.")
                print_stars()
                input()
                start_regular_node()
        else:
            try:
                option, timedOut = timedInteger(
                    "* Auto refresh disabled, Enter your menu choice: ",
                    timeout=-1,
                    resetOnInput=True,
                    allowNegative=False,
                )
                print_stars()
                menu_options[option]()
                if option != 1:
                    start_regular_node()
            except KeyError:
                print(f"* Bad option, try again. Press enter to continue.")
                print_stars()
                input()
                start_regular_node()


def service_menu_option() -> None:
    status = process_command("systemctl is-active --quiet harmony", True, False)
    if status == 0:
        print(
            f"*   8 - {Fore.RED}Stop Harmony Service      {Fore.GREEN}- {Fore.YELLOW}{Back.RED}WARNING: You will miss blocks while stopped!   {Style.RESET_ALL}{Fore.GREEN}"
        )
        print(
            f"*   9 - Restart Harmony Service   - {Back.RED}{Fore.YELLOW}WARNING: You will miss blocks during a restart!{Style.RESET_ALL}{Fore.GREEN}"
        )
    else:
        print(f"*   8 - Start Harmony Service")
    return


def hip_voting_option() -> None:
    # Specify the deadline in server's local time
    deadline = datetime(2023, 8, 9, 20, 59)

    # Get the current time in server's local time
    current_time = datetime.now()

    # Check if the current time is before or after the deadline
    active_vote = current_time < deadline

    if active_vote:
        print("*   7 - Harmony Governance Voting - Cast your vote for HIP-30v2")
    else:
        print("*   7 - Harmony Governance Voting - No votes currently active.")


def rewards_sender_option() -> None:
    if environ.get("REWARDS_WALLET"):
        print("*   5 - Send Wallet Balance       - Send your wallet balance - saved gas to rewards wallet")
        print("*   6 - Set Rewards Wallet        - Update your saved wallet or gas reserve")
    else:
        print("*   6 - Set Rewards Wallet        - Set up a one1 wallet address to send rewards when using option #4")
    return


def make_backup_dir() -> str:
    folder_name = f'{os.environ.get("HARMONY_DIR")}/harmony_backup/{datetime.now().strftime("%Y%m%d%H%M")}'
    process_command(f"mkdir -p {folder_name}")
    return folder_name


def hmy_cli_upgrade():
    question = ask_yes_no(
        "* Are you sure you would like to proceed with updating the Harmony CLI file?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        folder_name = make_backup_dir()
        process_command(f"cp {environ.get('HARMONY_DIR')}/hmy {folder_name}")
        print_stars()
        install_hmy()
        print_stars()
        print("Harmony cli has been updated to: ")
        process_command(f"{environ.get('HARMONY_DIR')}/hmy version")
        print_stars()
        set_var(EnvironmentVariables.dotenv_file, "HMY_UPGRADE_AVAILABLE", "False")
        input("* Update completed, press ENTER to return to the main menu. ")


def update_harmony_app():
    os.chdir(f"{os.environ.get('HARMONY_DIR')}")
    print_stars()
    print("Currently installed version: ")
    process_command("./harmony -V")
    folder_name = make_backup_dir()
    process_command(
        f"cp {os.environ.get('HARMONY_DIR')}/harmony {os.environ.get('HARMONY_DIR')}/harmony.conf {folder_name}"
    )
    print_stars()
    print("Downloading current harmony binary file from harmony.one: ")
    print_stars()
    pull_harmony_update(os.environ.get("HARMONY_DIR"), EnvironmentVariables.harmony_conf)
    print_stars()
    print("Updated version: ")
    process_command("./harmony -V")
    if environ.get("SHARD") != "0":
        size = 0
        for path, dirs, files in os.walk(f"{os.environ.get('HARMONY_DIR')}/harmony_db_0"):
            for f in files:
                fp = os.path.join(path, f)
                size += os.path.getsize(fp)
            if size >= 400000000:
                question = ask_yes_no(
                    Fore.WHITE
                    + "* Are you sure you would like to proceed with upgrading and trimming database 0?\n\nType 'Yes' or 'No' to continue"
                )
                if question:
                    process_command("sudo service harmony stop")
                    process_command(
                        f"mv {os.environ.get('HARMONY_DIR')}/harmony_db_0 {os.environ.get('HARMONY_DIR')}/harmony_db_0_old"
                    )
                    process_command("sudo service harmony start")
                    process_command(f"rm -r {os.environ.get('HARMONY_DIR')}/harmony_db_0_old")
                else:
                    print("Skipping removal of 0, but it's no longer required, fyi!")
            else:
                print("Your database 0 is already trimmed, enjoy!")
    process_command("sudo service harmony restart")
    print_stars()
    print("Harmony Service is restarting, waiting 10 seconds for restart.")
    set_var(EnvironmentVariables.dotenv_file, "HARMONY_UPGRADE_AVAILABLE", "False")
    time.sleep(10)


def menu_validator_stats():
    load_var_file(EnvironmentVariables.dotenv_file)
    remote_shard_0 = [
        f"{environ.get('HARMONY_DIR')}/hmy",
        "blockchain",
        "latest-headers",
        f'--node=https://api.s0.{environ.get("NETWORK_SWITCH")}.hmny.io',
    ]
    try:
        result_remote_shard_0 = run(remote_shard_0, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        remote_data_shard_0 = json.loads(result_remote_shard_0.stdout)
    except (ValueError, KeyError, TypeError) as e:
        print(f"* Remote Shard 0 Offline, Error {e}")
    try:
        http_port = find_port(environ.get("HARMONY_DIR"))
        local_shard = [
            f"{environ.get('HARMONY_DIR')}/hmy",
            "blockchain",
            "latest-headers",
            "--node",
            f"http://localhost:{http_port}",
        ]
        result_local_shard = run(local_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        local_data_shard = json.loads(result_local_shard.stdout)
    except (ValueError, KeyError, TypeError) as e:
        print(
            f"* Local Server Offline\n*\n* Run troubleshooting, See our documents site for info on how to manually troubleshoot:\n* https://docs.easynode.pro/harmony/post#validator-toolbox-troubleshooting\n*"
        )
        print_stars()
        finish_node()

    if environ.get("SHARD") != "0":
        remote_shard = [
            f"{environ.get('HARMONY_DIR')}/hmy",
            "blockchain",
            "latest-headers",
            f'--node=https://api.s{environ.get("SHARD")}.{environ.get("NETWORK_SWITCH")}.hmny.io',
        ]
        try:
            result_remote_shard = run(remote_shard, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            remote_data_shard = json.loads(result_remote_shard.stdout)
            return remote_data_shard_0, local_data_shard, remote_data_shard
        except (ValueError, KeyError, TypeError):
            return

    return remote_data_shard_0, local_data_shard, None


def shard_stats(our_shard) -> str:
    our_uptime = subprocess.getoutput("uptime")
    db_0_size = get_db_size(os.environ.get("HARMONY_DIR"), "0")
    if our_shard == "0":
        print(
            f"""
    * Uptime :: {our_uptime}\n\n Harmony DB 0 Size  ::  {db_0_size}
    {string_stars()}
        """
        )
    else:
        print(
            f"""
    * Uptime :: {our_uptime}
    *
    * Harmony DB 0 Size  ::  {db_0_size}
    * Harmony DB {our_shard} Size  ::   {get_db_size(os.environ.get("HARMONY_DIR"), str(our_shard))}
    *
    *
    {string_stars()}
        """
        )


def harmony_binary_upgrade():
    question = ask_yes_no(
        Fore.RED
        + "* WARNING: YOU WILL MISS BLOCKS WHILE YOU UPGRADE THE HARMONY SERVICE.\n\n"
        + Fore.WHITE
        + "* Are you sure you would like to proceed?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        update_harmony_app()


def menu_service_stop_start() -> str:
    status = process_command("systemctl is-active --quiet harmony")
    if status != 0:
        process_command("sudo service harmony start")
        print()
        print("* Harmony Service Has Been Started.")
        print()
        input("* Press ENTER to return to the main menu.")
    else:
        question = ask_yes_no(
            "*********\n"
            + Fore.RED
            + "* WARNING: YOU WILL MISS BLOCKS IF YOU STOP THE HARMONY SERVICE.\n\n"
            + Fore.WHITE
            + "* Are you sure you would like to proceed?\n\nType 'Yes' or 'No' to continue"
        )
        if question:
            process_command("sudo service harmony stop")
            print()
            print(
                "* Harmony Service Has Been Stopped. "
                + Fore.RED
                + "YOU ARE MISSING BLOCKS ON THIS NODE."
                + Style.RESET_ALL
                + Fore.GREEN
            )
            print()
            input("* Press ENTER to return to the main menu.")


def menu_service_restart() -> str:
    question = ask_yes_no(
        "*********\n"
        + Fore.RED
        + "WARNING: YOU WILL MISS BLOCKS UNTIL RESTART IS COMPLETED & SYNC CATCHES UP!\n\n"
        + Fore.WHITE
        + "Are you sure you would like to proceed?\n\nType 'Yes' or 'No' to continue"
    )
    if question:
        process_command("sudo service harmony restart")
        print()
        print("* The Harmony Service Has Been Restarted")
        input("* Press ENTER to return to the main menu.")


def menu_active_bls() -> str:
    validator_wallet = environ.get("VALIDATOR_WALLET")
    json_response = get_wallet_json(validator_wallet)
    print("* This is a list of your BLS Keys that are active for the next election.")
    for i, x in enumerate(json_response["bls-public-keys"]):
        print(f"BLS Key {i+1} {x}")
    print_stars()
    print("* Press ENTER to return to the main menu.")
    print_stars()
    input()


# is this used?
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def menu_check_balance(rpc, validator_wallet) -> None:
    if environ.get("NODE_TYPE") == "regular":
        print("* Calling mainnet and testnet for balances...")
        print_stars()
        total_balance, total_balance_test = get_wallet_balance(validator_wallet)
        print(f"* Your Validator Wallet Balance on Mainnet is: {total_balance} Harmony ONE Coins")
        print(f"* Your Pending Validator Rewards are: {get_rewards_balance(rpc, validator_wallet)}")
        print(f"* Your Validator Wallet Balance on Testnet is: {total_balance_test} Harmony ONE Test Coins")
        print_stars()
        i = 0
        while i < 1:
            question = ask_yes_no("* Would you like to check another Harmony ONE Address? (YES/NO) ")
            if question:
                balanceCheckAny()
            else:
                i = 1
    else:
        i = 0
        while i < 1:
            question = ask_yes_no("* Would you like to check a Harmony ONE Address? (YES/NO) ")
            if question:
                balanceCheckAny()
            else:
                i = 1


def balanceCheckAny():
    check_wallet = input(
        "* Type the address of the Harmony ONE Wallet you would like to check.\n"
        + "* Only one wallets will work, no 0x addresses : "
    )
    print("* Calling mainnet and testnet for balances...")
    print_stars()
    total_balance, total_balance_test = get_wallet_balance(check_wallet)
    print(
        f"* The Mainnet Wallet Balance is: {total_balance} Harmony ONE Coins\n* The Testnet Wallet Balance is: {total_balance_test} Harmony ONE Test Coins"
    )
    print_stars()
    input("* Press ENTER to continue.")


def get_current_epoch():
    config = EnvironmentVariables()
    current_epoch = 0
    try:
        current_epoch = blockchain.get_current_epoch(config.working_rpc_endpoint)
        return current_epoch
    except Exception as e:
        print(f"* Error getting current epoch: {e}")
        return current_epoch
