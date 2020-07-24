import click
import requests
import time
from os import path, startfile
from win10toast import ToastNotifier
from click_shell import shell

# Gets path to current directory
dirpath = path.dirname(path.abspath(__file__))
# Windows popup notifier
toaster = ToastNotifier()
# Sites that are unavailable
unavailable_sites = []
saved_sites = []

# If there are any saved sites, add them to the list of urls to check
if path.isfile(f'{dirpath}\sites.txt'):
    with open(f'{dirpath}\sites.txt', 'r') as file:
        tempSites = file.read().split(',')
        saved_sites = [s for s in tempSites if s.strip()]


# Using click_shell
@shell(prompt="\n>>> ")
def cli():
    pass


@cli.command(help="add a site to the list of sites to check")
@click.argument('site_url')
def add(site_url):
    """Adds a site url to saved_sites list and sites.txt"""

    saved_sites.append(site_url)
    save_sites()
    click.echo(f"added {site_url}")


@cli.command(help="remove a site from the list of sites to check")
@click.argument('site_url')
def remove(site_url):
    """removes a site url from saved_sites var and sites.txt"""

    saved_sites.remove(site_url)
    save_sites()
    click.echo(f"removed {site_url}")


@cli.command(help="check site availability once")
@click.option("-s", "--site", 'site', default=None, help="specific site to check")
def check(site):
    """
        Checks all saved sites (or one specified site)
        once and calls perform_check()
    """

    if len(saved_sites) == 0:
        return click.secho("you have not given any sites to check", fg='red')

    with open(f'{dirpath}\log.txt', 'a') as logFile:
        logFile.write('\n\n' + str(time.strftime('%Y-%m-%d %H:%M', time.localtime())))
        if site is None:
            for s in saved_sites:
                perform_check(logFile, s)
        else:
            perform_check(logFile, site)


@cli.command(help="monitor site availability at regular intervals")
@click.option("-s", "--site", 'site', default=None, help="specific site to check")
@click.option("-i", "--interval", 'interval', default=600, show_default=True, help="how often (in sec) to check sites")
def monitor(site, interval):
    """
        Checks all saved sites (or one specified site)
        at regular intervals and calls perform_check()
    """

    if len(saved_sites) == 0:
        return click.secho("you have not given any sites to monitor", fg='red')

    while True:
        with open(f'{dirpath}\log.txt', 'a') as logFile:
            logFile.write('\n\n' + str(time.strftime('%Y-%m-%d %H:%M', time.localtime())))
            if site is None:
                for s in saved_sites:
                    perform_check(logFile, s)
            else:
                perform_check(logFile, site)
        time.sleep(interval)


@cli.command()
def sites():
    """Prints saved sites in console"""

    if len(saved_sites) > 0:
        for site in saved_sites:
            click.echo(site)
    else:
        click.secho("no saved sites yet exist", fg='red')


@cli.command()
def log():
    """Opens log.txt in the default editor"""

    if path.isfile(f'{dirpath}\log.txt'):
        startfile(f'{dirpath}\log.txt')
    else:
        click.secho("no log yet exists", fg='red')


def save_sites():
    """Saves sites to sitex.txt"""
    
    with open(f'{dirpath}\sites.txt', 'w') as f:
        for site in saved_sites:
            f.write(site + ',')


def perform_check(logFile, site):
    """
        Performs a check on the given site,
        writes the result in the console and log.txt

        If nececeary sends a notification

        Args:
            logFile (TextIOWrapper): log.txt file
            site    (str):           site url
    """

    def get_status_code(site):
        """
            Sends a get request to site and returns the status code

            Returns: response status code
        """

        try:
            response = requests.get(site)
            return response.status_code
        except requests.exceptions.ConnectionError:
            time.sleep(5)

    def chck_status_code(site, status_code):
        """
            Checks if site is avaivable

            Returns: bool for write status method
        
            If the site is unavailable,
            append to unavailable_sites list

            If the site was unavailable but is now,
            remove from unavailable_sites list and return True
        """

        if site in unavailable_sites and status_code < 400:
            unavailable_sites.remove(site)
            return True
        elif status_code > 399:
            unavailable_sites.append(site)
        return False

    def write_status(logfile, site, avaivable_again, status_code):
        """
            Writes result in console and to log.txt

            If the site was unavailable but is now,
            show notification and print special line in console
        """

        logfile.write(f"\n\t{site} : {status_code}")
        if avaivable_again == True:
            toaster.show_toast(
                f"{site} is now available",
                f"{site}: {status_code}",
                threaded=True,
                icon_path=None,
                duration=6
            )
            # To make sure notifications don't owerlap
            while toaster.notification_active():
                time.sleep(0.1)
            return click.secho(
                f"{site} is now available : {status_code}",
                fg='green'
        )
        click.echo(f"{site} : {status_code}")

    status_code = get_status_code(site)
    avaivable_again = chck_status_code(site, status_code)
    write_status(logFile, site, avaivable_again, status_code)
