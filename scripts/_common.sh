#!/bin/bash

#=================================================
# ARGUMENTS FROM CONFIG PANEL
#=================================================

debug_enabled="0"  # "1" or "0" string
log_level="WARNING"
admin_email="${admin}@${domain}"
default_from_email="${app}@${domain}"

#=================================================
# SET CONSTANTS
#=================================================

XDG_CACHE_HOME="$data_dir/.cache/"
log_path="/var/log/$app"
log_file="${log_path}/${app}.log"

#=================================================
# HELPERS
#=================================================

myynh_setup_python_venv() {
    ynh_print_info "Creating Python virtualenv for $app..."

    # Crée l’environnement virtuel avec Python système
    python3 -m venv "$data_dir/.venv"

    ynh_print_info "Activating virtualenv and installing dependencies..."

    # Active le venv
    source "$data_dir/.venv/bin/activate"

    # Upgrade pip et outils de build
    pip install --upgrade pip wheel setuptools

    # Installe les dépendances
    pip install --no-deps -r "$data_dir/requirements.txt"
}

myynh_setup_log_file() {
    mkdir -p "$(dirname "$log_file")"
    touch "$log_file"

    chown -c -R $app:$app "$log_path"
    chmod -c u+rwx,o-rwx "$log_path"
}

myynh_fix_file_permissions() {
    # Dossier de l'application (statique, nginx)
    chown -c -R "$app:www-data" "$install_dir"
    chmod -c u+rwx,g+rx,o-rwx "$install_dir"

    # Dossier data de l'app (venv, configs, etc.)
    chown -c -R "$app:$app" "$data_dir"
    chmod -c u+rwx,g+rx,o-rwx "$data_dir"
}