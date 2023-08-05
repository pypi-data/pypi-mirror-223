from insights.core.spec_factory import SpecSet, RegistryPoint


class Specs(SpecSet):
    # Client App specs
    malware_detection = RegistryPoint()

    # Regular collection specs
    abrt_ccpp_conf = RegistryPoint(filterable=True)
    abrt_status_bare = RegistryPoint()
    alternatives_display_python = RegistryPoint()
    amq_broker = RegistryPoint(multi_output=True)
    ansible_host = RegistryPoint()
    audit_log = RegistryPoint(filterable=True)
    auditctl_rules = RegistryPoint()
    auditctl_status = RegistryPoint()
    auditd_conf = RegistryPoint()
    audispd_conf = RegistryPoint()
    authselect_current = RegistryPoint()
    autofs_conf = RegistryPoint()
    avc_cache_threshold = RegistryPoint()
    avc_hash_stats = RegistryPoint()
    aws_instance_id_doc = RegistryPoint()
    aws_instance_id_pkcs7 = RegistryPoint()
    aws_public_ipv4_addresses = RegistryPoint()
    aws_public_hostnames = RegistryPoint()
    awx_manage_check_license = RegistryPoint()
    awx_manage_check_license_data = RegistryPoint(filterable=True)
    awx_manage_print_settings = RegistryPoint()
    azure_instance_id = RegistryPoint()
    azure_instance_plan = RegistryPoint()
    azure_instance_type = RegistryPoint()
    azure_load_balancer = RegistryPoint()
    bdi_read_ahead_kb = RegistryPoint(multi_output=True)
    bios_uuid = RegistryPoint()
    blacklisted_specs = RegistryPoint()
    blkid = RegistryPoint()
    bond = RegistryPoint(multi_output=True)
    bond_dynamic_lb = RegistryPoint(multi_output=True)
    boot_loader_entries = RegistryPoint(multi_output=True)
    branch_info = RegistryPoint(raw=True)
    brctl_show = RegistryPoint()
    candlepin_broker = RegistryPoint()
    candlepin_error_log = RegistryPoint(filterable=True)
    candlepin_log = RegistryPoint(filterable=True)
    catalina_out = RegistryPoint(multi_output=True, filterable=True)
    catalina_server_log = RegistryPoint(multi_output=True, filterable=True)
    cciss = RegistryPoint(multi_output=True)
    cdc_wdm = RegistryPoint()
    ceilometer_central_log = RegistryPoint(filterable=True)
    ceilometer_collector_log = RegistryPoint(filterable=True)
    ceilometer_compute_log = RegistryPoint(filterable=True)
    ceilometer_conf = RegistryPoint()
    ceph_conf = RegistryPoint(filterable=True)
    ceph_config_show = RegistryPoint(multi_output=True)
    ceph_df_detail = RegistryPoint()
    ceph_health_detail = RegistryPoint()
    ceph_insights = RegistryPoint()
    ceph_log = RegistryPoint(multi_output=True, filterable=True)
    ceph_osd_df = RegistryPoint()
    ceph_osd_dump = RegistryPoint()
    ceph_osd_ec_profile_get = RegistryPoint(multi_output=True)
    ceph_osd_ec_profile_ls = RegistryPoint()
    ceph_osd_log = RegistryPoint(multi_output=True, filterable=True)
    ceph_osd_tree = RegistryPoint()
    ceph_osd_tree_text = RegistryPoint()
    ceph_report = RegistryPoint()
    ceph_s = RegistryPoint()
    ceph_v = RegistryPoint()
    certificates_enddate = RegistryPoint()
    cgroups = RegistryPoint()
    checkin_conf = RegistryPoint()
    chkconfig = RegistryPoint()
    chrony_conf = RegistryPoint()
    chronyc_sources = RegistryPoint()
    cib_xml = RegistryPoint()
    cinder_api_log = RegistryPoint(filterable=True)
    cinder_conf = RegistryPoint()
    cinder_volume_log = RegistryPoint(filterable=True)
    cloud_cfg = RegistryPoint(filterable=True)
    cloud_cfg_filtered = RegistryPoint()
    cloud_init_custom_network = RegistryPoint()
    cloud_init_log = RegistryPoint(filterable=True)
    cluster_conf = RegistryPoint(filterable=True)
    cmdline = RegistryPoint()
    cni_podman_bridge_conf = RegistryPoint()
    cobbler_modules_conf = RegistryPoint()
    cobbler_settings = RegistryPoint()
    containers_policy = RegistryPoint()
    corosync = RegistryPoint()
    corosync_cmapctl = RegistryPoint(multi_output=True)
    corosync_conf = RegistryPoint()
    cpe = RegistryPoint()
    cpu_cores = RegistryPoint(multi_output=True)
    cpu_siblings = RegistryPoint(multi_output=True)
    cpu_smt_active = RegistryPoint()
    cpu_smt_control = RegistryPoint()
    cpu_vulns = RegistryPoint(multi_output=True)
    cpuinfo = RegistryPoint()
    cpuinfo_max_freq = RegistryPoint()
    cpupower_frequency_info = RegistryPoint()
    cpuset_cpus = RegistryPoint()
    crictl_logs = RegistryPoint(multi_output=True, filterable=True)
    crio_conf = RegistryPoint(multi_output=True)
    cron_daily_rhsmd = RegistryPoint(filterable=True)
    cron_foreman = RegistryPoint(filterable=True)
    crt = RegistryPoint()
    crypto_policies_bind = RegistryPoint()
    crypto_policies_config = RegistryPoint()
    crypto_policies_opensshserver = RegistryPoint()
    crypto_policies_state_current = RegistryPoint()
    cryptsetup_luksDump = RegistryPoint(multi_output=True)
    cupsd_conf = RegistryPoint()
    cups_files_conf = RegistryPoint()
    cups_ppd = RegistryPoint(multi_output=True)
    current_clocksource = RegistryPoint()
    date = RegistryPoint()
    date_iso = RegistryPoint()
    date_utc = RegistryPoint()
    db2ls_a_c = RegistryPoint()
    dcbtool_gc_dcb = RegistryPoint(multi_output=True)
    designate_conf = RegistryPoint(filterable=True)
    df__al = RegistryPoint()
    df__alP = RegistryPoint()
    df__li = RegistryPoint()
    dig = RegistryPoint()
    dig_dnssec = RegistryPoint()
    dig_edns = RegistryPoint()
    dig_noedns = RegistryPoint()
    dirsrv = RegistryPoint()
    dirsrv_access = RegistryPoint(multi_output=True, filterable=True)
    dirsrv_errors = RegistryPoint(multi_output=True, filterable=True)
    display_java = RegistryPoint()
    display_name = RegistryPoint()
    dm_mod_use_blk_mq = RegistryPoint()
    dmesg = RegistryPoint(filterable=True)
    dmesg_log = RegistryPoint(filterable=True)
    dmidecode = RegistryPoint()
    dmsetup_info = RegistryPoint()
    dmsetup_status = RegistryPoint()
    dnf_conf = RegistryPoint(filterable=True)
    dnf_module_info = RegistryPoint()
    dnf_module_list = RegistryPoint()
    dnf_modules = RegistryPoint(multi_output=True)
    dnsmasq_config = RegistryPoint(multi_output=True)
    docker_container_inspect = RegistryPoint(multi_output=True)
    docker_host_machine_id = RegistryPoint()
    docker_image_inspect = RegistryPoint(multi_output=True)
    docker_info = RegistryPoint()
    docker_list_containers = RegistryPoint()
    docker_list_images = RegistryPoint()
    docker_network = RegistryPoint()
    docker_storage = RegistryPoint()
    docker_storage_setup = RegistryPoint()
    docker_sysconfig = RegistryPoint()
    dotnet_version = RegistryPoint()
    doveconf = RegistryPoint(filterable=True)
    dracut_kdump_capture_service = RegistryPoint()
    dse_ldif = RegistryPoint(multi_output=True, filterable=True)
    du_dirs = RegistryPoint(multi_output=True, filterable=True)
    dumpe2fs_h = RegistryPoint(multi_output=True)
    duplicate_machine_id = RegistryPoint(filterable=True)
    eap_json_reports = RegistryPoint(multi_output=True)
    engine_config_all = RegistryPoint()
    engine_db_query_vdsm_version = RegistryPoint()
    engine_log = RegistryPoint(filterable=True)
    etc_journald_conf = RegistryPoint()
    etc_journald_conf_d = RegistryPoint(multi_output=True)
    etc_machine_id = RegistryPoint()
    etc_udev_40_redhat_rules = RegistryPoint(filterable=True)
    etc_udev_oracle_asm_rules = RegistryPoint(multi_output=True, filterable=True)
    etcd_conf = RegistryPoint(filterable=True)
    ethtool = RegistryPoint(multi_output=True)
    ethtool_S = RegistryPoint(multi_output=True)
    ethtool_T = RegistryPoint(multi_output=True)
    ethtool_a = RegistryPoint(multi_output=True)
    ethtool_c = RegistryPoint(multi_output=True)
    ethtool_g = RegistryPoint(multi_output=True)
    ethtool_i = RegistryPoint(multi_output=True)
    ethtool_k = RegistryPoint(multi_output=True)
    exim_conf = RegistryPoint()
    facter = RegistryPoint()
    fapolicyd_rules = RegistryPoint(multi_output=True, filterable=True)
    fc_match = RegistryPoint()
    fcoeadm_i = RegistryPoint()
    fdisk_l = RegistryPoint()
    fdisk_l_sos = RegistryPoint(multi_output=True)
    findmnt_lo_propagation = RegistryPoint()
    firewall_cmd_list_all_zones = RegistryPoint()
    firewalld_conf = RegistryPoint(filterable=True)
    foreman_production_log = RegistryPoint(filterable=True)
    foreman_proxy_conf = RegistryPoint()
    foreman_proxy_log = RegistryPoint(filterable=True)
    foreman_rake_db_migrate_status = RegistryPoint()
    foreman_satellite_log = RegistryPoint(filterable=True)
    foreman_ssl_access_ssl_log = RegistryPoint(filterable=True)
    foreman_ssl_error_ssl_log = RegistryPoint(filterable=True)
    foreman_tasks_config = RegistryPoint(filterable=True)
    freeipa_healthcheck_log = RegistryPoint()
    fstab = RegistryPoint()
    fw_devices = RegistryPoint()
    fw_security = RegistryPoint()
    galera_cnf = RegistryPoint()
    gcp_instance_type = RegistryPoint()
    gcp_license_codes = RegistryPoint()
    gcp_network_interfaces = RegistryPoint()
    getcert_list = RegistryPoint()
    getconf_page_size = RegistryPoint()
    getenforce = RegistryPoint()
    getsebool = RegistryPoint()
    gfs2_file_system_block_size = RegistryPoint(multi_output=True)
    glance_api_conf = RegistryPoint()
    glance_api_log = RegistryPoint(filterable=True)
    glance_cache_conf = RegistryPoint()
    glance_registry_conf = RegistryPoint()
    gluster_peer_status = RegistryPoint()
    gluster_v_info = RegistryPoint()
    gluster_v_status = RegistryPoint()
    gnocchi_conf = RegistryPoint(filterable=True)
    gnocchi_metricd_log = RegistryPoint(filterable=True)
    greenboot_status = RegistryPoint(filterable=True)
    group_info = RegistryPoint(filterable=True)
    grub1_config_perms = RegistryPoint()
    grub2_cfg = RegistryPoint()
    grub2_efi_cfg = RegistryPoint()
    grub_conf = RegistryPoint()
    grub_config_perms = RegistryPoint()
    grub_efi_conf = RegistryPoint()
    grubby_default_index = RegistryPoint()
    grubby_default_kernel = RegistryPoint()
    grubenv = RegistryPoint()
    hammer_ping = RegistryPoint()
    hammer_task_list = RegistryPoint()
    haproxy_cfg = RegistryPoint()
    haproxy_cfg_scl = RegistryPoint()
    heat_api_log = RegistryPoint(filterable=True)
    heat_conf = RegistryPoint()
    heat_crontab = RegistryPoint()
    heat_crontab_container = RegistryPoint()
    heat_engine_log = RegistryPoint(filterable=True)
    hostname = RegistryPoint()
    hostname_default = RegistryPoint()
    hostname_short = RegistryPoint()
    hosts = RegistryPoint()
    hponcfg_g = RegistryPoint()
    httpd24_httpd_error_log = RegistryPoint(filterable=True)
    httpd_M = RegistryPoint(multi_output=True)
    httpd_V = RegistryPoint(multi_output=True)
    httpd_access_log = RegistryPoint(filterable=True)
    httpd_cert_info_in_nss = RegistryPoint(multi_output=True, filterable=True)
    httpd_conf = RegistryPoint(multi_output=True)
    httpd_conf_scl_httpd24 = RegistryPoint(multi_output=True)
    httpd_conf_scl_jbcs_httpd24 = RegistryPoint(multi_output=True)
    httpd_error_log = RegistryPoint(filterable=True)
    httpd_limits = RegistryPoint(multi_output=True)
    httpd_on_nfs = RegistryPoint()
    httpd_ssl_access_log = RegistryPoint(filterable=True)
    httpd_ssl_cert_enddate = RegistryPoint(multi_output=True)
    httpd_ssl_error_log = RegistryPoint(filterable=True)
    ibm_fw_vernum_encoded = RegistryPoint()
    ibm_lparcfg = RegistryPoint(filterable=True)
    ifcfg = RegistryPoint(multi_output=True)
    ifcfg_static_route = RegistryPoint(multi_output=True)
    ifconfig = RegistryPoint()
    imagemagick_policy = RegistryPoint(multi_output=True, filterable=True)
    init_ora = RegistryPoint()
    init_process_cgroup = RegistryPoint()
    initctl_lst = RegistryPoint()
    initscript = RegistryPoint(multi_output=True)
    insights_client_conf = RegistryPoint(filterable=True)
    insights_client_exp_sed = RegistryPoint()  # INSPEC-414
    installed_rpms = RegistryPoint()
    interrupts = RegistryPoint()
    ip6tables = RegistryPoint()
    ip6tables_permanent = RegistryPoint()
    ip_addr = RegistryPoint()
    ip_addresses = RegistryPoint()
    ip_neigh_show = RegistryPoint()
    ip_netns_exec_namespace_lsof = RegistryPoint(multi_output=True, filterable=True)
    ip_route_show_table_all = RegistryPoint()
    ip_s_link = RegistryPoint()
    ipa_default_conf = RegistryPoint()
    ipaupgrade_log = RegistryPoint(filterable=True)
    ipcs_m = RegistryPoint()
    ipcs_m_p = RegistryPoint()
    ipcs_s = RegistryPoint()
    ipcs_s_i = RegistryPoint(multi_output=True)
    ipsec_conf = RegistryPoint(filterable=True)
    iptables = RegistryPoint()
    iptables_permanent = RegistryPoint()
    ipv4_neigh = RegistryPoint()
    ipv6_neigh = RegistryPoint()
    iris_cpf = RegistryPoint()
    iris_list = RegistryPoint()
    iris_messages_log = RegistryPoint(filterable=True)
    ironic_conf = RegistryPoint(filterable=True)
    ironic_inspector_log = RegistryPoint(filterable=True)
    iscsiadm_m_session = RegistryPoint()
    jbcs_httpd24_httpd_error_log = RegistryPoint(filterable=True)
    jboss_domain_server_log = RegistryPoint(multi_output=True, filterable=True)
    jboss_runtime_versions = RegistryPoint()
    jboss_standalone_main_config = RegistryPoint(multi_output=True)
    jboss_standalone_server_log = RegistryPoint(multi_output=True, filterable=True)
    jboss_version = RegistryPoint(multi_output=True)
    journal_all = RegistryPoint(filterable=True)
    journal_header = RegistryPoint(filterable=True)
    journal_since_boot = RegistryPoint(filterable=True)
    katello_service_status = RegistryPoint(filterable=True)
    kdump_conf = RegistryPoint()
    kerberos_kdc_log = RegistryPoint(filterable=True)
    kernel_config = RegistryPoint(multi_output=True, filterable=True)
    kernel_crash_kexec_post_notifiers = RegistryPoint()
    kexec_crash_loaded = RegistryPoint()
    kexec_crash_size = RegistryPoint()
    keystone_conf = RegistryPoint()
    keystone_crontab = RegistryPoint()
    keystone_crontab_container = RegistryPoint()
    keystone_log = RegistryPoint(filterable=True)
    kpatch_list = RegistryPoint()
    krb5 = RegistryPoint(multi_output=True)
    ksmstate = RegistryPoint()
    ktimer_lockless = RegistryPoint()
    kubepods_cpu_quota = RegistryPoint(multi_output=True)
    lastupload = RegistryPoint(multi_output=True)
    leapp_report = RegistryPoint()
    ld_library_path_of_user = RegistryPoint()
    ldif_config = RegistryPoint(multi_output=True)
    libssh_client_config = RegistryPoint(filterable=True)
    libssh_server_config = RegistryPoint(filterable=True)
    libvirtd_log = RegistryPoint(filterable=True)
    libvirtd_qemu_log = RegistryPoint(multi_output=True, filterable=True)
    limits_conf = RegistryPoint(multi_output=True)
    locale = RegistryPoint()
    localtime = RegistryPoint()
    logrotate_conf = RegistryPoint(multi_output=True)
    losetup = RegistryPoint()
    lpfc_max_luns = RegistryPoint()
    lpstat_p = RegistryPoint()
    lpstat_protocol_printers = RegistryPoint()
    # New `ls` Specs
    ls_la = RegistryPoint()
    ls_la_dirs = RegistryPoint(filterable=True)
    ls_la_filtered = RegistryPoint(filterable=True)
    ls_la_filtered_dirs = RegistryPoint(filterable=True)
    ls_lan = RegistryPoint()
    ls_lan_dirs = RegistryPoint(filterable=True)
    ls_lan_filtered = RegistryPoint(filterable=True)
    ls_lan_filtered_dirs = RegistryPoint(filterable=True)
    ls_lanL = RegistryPoint()
    ls_lanL_dirs = RegistryPoint(filterable=True)
    ls_lanR = RegistryPoint()
    ls_lanR_dirs = RegistryPoint(filterable=True)
    ls_lanRL = RegistryPoint()
    ls_lanRL_dirs = RegistryPoint(filterable=True)
    ls_lanRZ = RegistryPoint()
    ls_lanRZ_dirs = RegistryPoint(filterable=True)
    ls_lanZ = RegistryPoint()
    ls_lanZ_dirs = RegistryPoint(filterable=True)
    # Old `ls` Specs
    ls_R_var_lib_nova_instances = RegistryPoint()
    ls_boot = RegistryPoint()
    ls_dev = RegistryPoint()
    ls_disk = RegistryPoint()
    ls_docker_volumes = RegistryPoint()
    ls_edac_mc = RegistryPoint()
    ls_etc = RegistryPoint()
    ls_etc_ssh = RegistryPoint()
    ls_ipa_idoverride_memberof = RegistryPoint()
    ls_krb5_sssd = RegistryPoint()
    ls_lib_firmware = RegistryPoint()
    ls_ocp_cni_openshift_sdn = RegistryPoint()
    ls_origin_local_volumes_pods = RegistryPoint()
    ls_osroot = RegistryPoint()
    ls_rsyslog_errorfile = RegistryPoint()
    ls_sys_firmware = RegistryPoint()
    ls_systemd_units = RegistryPoint()
    ls_tmp = RegistryPoint(filterable=True)
    ls_usr_bin = RegistryPoint(filterable=True)
    ls_usr_lib64 = RegistryPoint(filterable=True)
    ls_usr_sbin = RegistryPoint(filterable=True)
    ls_var_cache_pulp = RegistryPoint()
    ls_var_lib_mongodb = RegistryPoint()
    ls_var_lib_nova_instances = RegistryPoint()
    ls_var_lib_pcp = RegistryPoint()
    ls_var_lib_rpm = RegistryPoint()
    ls_var_lib_rsyslog = RegistryPoint()
    ls_var_log = RegistryPoint()
    ls_var_opt_mssql = RegistryPoint()
    ls_var_opt_mssql_log = RegistryPoint()
    ls_var_run = RegistryPoint()
    ls_var_spool_clientmq = RegistryPoint()
    ls_var_spool_postfix_maildrop = RegistryPoint()
    ls_var_tmp = RegistryPoint(filterable=True)
    ls_var_www = RegistryPoint()
    lsblk = RegistryPoint()
    lsblk_pairs = RegistryPoint()
    lscpu = RegistryPoint()
    lsinitrd = RegistryPoint(filterable=True)
    lsinitrd_kdump_image = RegistryPoint(filterable=True)
    lsinitrd_lvm_conf = RegistryPoint(filterable=True)
    lsmod = RegistryPoint()
    lsof = RegistryPoint(filterable=True)
    lspci = RegistryPoint()
    lspci_vmmkn = RegistryPoint()
    lssap = RegistryPoint()
    lsscsi = RegistryPoint()
    luksmeta = RegistryPoint(multi_output=True)
    lvdisplay = RegistryPoint()
    lvm_conf = RegistryPoint(filterable=True)
    lvm_system_devices = RegistryPoint()
    lvmconfig = RegistryPoint()
    lvs_headings = RegistryPoint()
    lvs_noheadings = RegistryPoint()
    lvs_noheadings_all = RegistryPoint()
    mac_addresses = RegistryPoint(multi_output=True)
    machine_id = RegistryPoint()
    manila_conf = RegistryPoint()
    mariadb_log = RegistryPoint(filterable=True)
    max_uid = RegistryPoint()
    md5chk_files = RegistryPoint(multi_output=True)
    mdadm_E = RegistryPoint(multi_output=True)
    mdstat = RegistryPoint()
    meminfo = RegistryPoint()
    messages = RegistryPoint(filterable=True)
    metadata_json = RegistryPoint(raw=True)
    mistral_executor_log = RegistryPoint(filterable=True)
    mlx4_port = RegistryPoint(multi_output=True)
    modinfo_filtered_modules = RegistryPoint()
    modinfo_modules = RegistryPoint(filterable=True)
    modprobe = RegistryPoint(multi_output=True)
    mokutil_sbstate = RegistryPoint()
    mongod_conf = RegistryPoint(multi_output=True, filterable=True)
    mount = RegistryPoint()
    mountinfo = RegistryPoint()
    mounts = RegistryPoint()
    mpirun_version = RegistryPoint()
    mssql_api_assessment = RegistryPoint()
    mssql_conf = RegistryPoint()
    mssql_tls_cert_enddate = RegistryPoint()
    multicast_querier = RegistryPoint()
    multipath__v4__ll = RegistryPoint()
    multipath_conf = RegistryPoint()
    multipath_conf_initramfs = RegistryPoint()
    mysql_log = RegistryPoint(multi_output=True, filterable=True)
    mysqladmin_status = RegistryPoint()
    mysqladmin_vars = RegistryPoint()
    mysqld_limits = RegistryPoint()
    named_checkconf_p = RegistryPoint(filterable=True)
    named_conf = RegistryPoint(filterable=True)
    namespace = RegistryPoint()
    ndctl_list_Ni = RegistryPoint()
    netconsole = RegistryPoint()
    netstat = RegistryPoint()
    netstat_agn = RegistryPoint()
    netstat_i = RegistryPoint()
    netstat_s = RegistryPoint()
    networkmanager_conf = RegistryPoint()
    networkmanager_dispatcher_d = RegistryPoint(multi_output=True)
    neutron_conf = RegistryPoint(filterable=True)
    neutron_dhcp_agent_ini = RegistryPoint(filterable=True)
    neutron_l3_agent_ini = RegistryPoint(filterable=True)
    neutron_l3_agent_log = RegistryPoint(filterable=True)
    neutron_metadata_agent_ini = RegistryPoint(filterable=True)
    neutron_metadata_agent_log = RegistryPoint(filterable=True)
    neutron_ml2_conf = RegistryPoint(filterable=True)
    neutron_ovs_agent_log = RegistryPoint(filterable=True)
    neutron_plugin_ini = RegistryPoint()
    neutron_server_log = RegistryPoint(filterable=True)
    neutron_sriov_agent = RegistryPoint(filterable=True)
    nfnetlink_queue = RegistryPoint()
    nfs_conf = RegistryPoint()
    nfs_exports = RegistryPoint()
    nfs_exports_d = RegistryPoint(multi_output=True)
    nginx_conf = RegistryPoint(multi_output=True)
    nginx_error_log = RegistryPoint(filterable=True)
    nginx_ssl_cert_enddate = RegistryPoint(multi_output=True)
    nmcli_conn_show = RegistryPoint()
    nmcli_dev_show = RegistryPoint()
    nmcli_dev_show_sos = RegistryPoint(multi_output=True)
    nova_api_log = RegistryPoint(filterable=True)
    nova_compute_log = RegistryPoint(filterable=True)
    nova_conf = RegistryPoint()
    nova_crontab = RegistryPoint()
    nova_crontab_container = RegistryPoint()
    nova_migration_uid = RegistryPoint()
    nova_uid = RegistryPoint()
    nscd_conf = RegistryPoint(filterable=True)
    nss_rhel7 = RegistryPoint()
    nsswitch_conf = RegistryPoint(filterable=True)
    ntp_conf = RegistryPoint()
    ntpq_leap = RegistryPoint()
    ntpq_pn = RegistryPoint()
    ntptime = RegistryPoint()
    numa_cpus = RegistryPoint(multi_output=True)
    numeric_user_group_name = RegistryPoint()
    nvme_core_io_timeout = RegistryPoint()
    oc_get_bc = RegistryPoint()
    oc_get_build = RegistryPoint()
    oc_get_clusterrole_with_config = RegistryPoint()
    oc_get_clusterrolebinding_with_config = RegistryPoint()
    oc_get_configmap = RegistryPoint()
    oc_get_dc = RegistryPoint()
    oc_get_egressnetworkpolicy = RegistryPoint()
    oc_get_endpoints = RegistryPoint()
    oc_get_event = RegistryPoint()
    oc_get_node = RegistryPoint()
    oc_get_pod = RegistryPoint()
    oc_get_project = RegistryPoint()
    oc_get_pv = RegistryPoint()
    oc_get_pvc = RegistryPoint()
    oc_get_rc = RegistryPoint()
    oc_get_role = RegistryPoint()
    oc_get_rolebinding = RegistryPoint()
    oc_get_route = RegistryPoint()
    oc_get_service = RegistryPoint()
    octavia_conf = RegistryPoint(filterable=True)
    od_cpu_dma_latency = RegistryPoint()
    odbc_ini = RegistryPoint(filterable=True)
    odbcinst_ini = RegistryPoint()
    open_vm_tools_stat_raw_text_session = RegistryPoint()
    openshift_certificates = RegistryPoint(multi_output=True)
    openshift_fluentd_environ = RegistryPoint(multi_output=True)
    openshift_hosts = RegistryPoint(filterable=True)
    openshift_router_environ = RegistryPoint(multi_output=True)
    openvswitch_daemon_log = RegistryPoint(filterable=True)
    openvswitch_other_config = RegistryPoint()
    openvswitch_server_log = RegistryPoint(filterable=True)
    os_release = RegistryPoint()
    osa_dispatcher_log = RegistryPoint(filterable=True)
    ose_master_config = RegistryPoint()
    ose_node_config = RegistryPoint()
    ovirt_engine_boot_log = RegistryPoint(filterable=True)
    ovirt_engine_confd = RegistryPoint(multi_output=True)
    ovirt_engine_console_log = RegistryPoint(filterable=True)
    ovirt_engine_server_log = RegistryPoint(filterable=True)
    ovirt_engine_ui_log = RegistryPoint(filterable=True)
    ovs_appctl_fdb_show_bridge = RegistryPoint(multi_output=True)
    ovs_ofctl_dump_flows = RegistryPoint(multi_output=True)
    ovs_vsctl_list_bridge = RegistryPoint()
    ovs_vsctl_show = RegistryPoint()
    ovs_vswitchd_limits = RegistryPoint()
    pacemaker_log = RegistryPoint(filterable=True)
    package_provides_command = RegistryPoint(filterable=True)
    pam_conf = RegistryPoint()
    parted__l = RegistryPoint()
    partitions = RegistryPoint()
    passenger_status = RegistryPoint()
    password_auth = RegistryPoint()
    pci_rport_target_disk_paths = RegistryPoint()
    pcp_metrics = RegistryPoint()
    pcp_openmetrics_log = RegistryPoint(filterable=True)
    pcs_config = RegistryPoint()
    pcs_quorum_status = RegistryPoint()
    pcs_status = RegistryPoint()
    php_ini = RegistryPoint(filterable=True)
    pluginconf_d = RegistryPoint(multi_output=True)
    pmlog_summary = RegistryPoint()
    pmrep_metrics = RegistryPoint()
    podman_container_inspect = RegistryPoint(multi_output=True)
    podman_image_inspect = RegistryPoint(multi_output=True)
    podman_list_containers = RegistryPoint()
    podman_list_images = RegistryPoint()
    postconf = RegistryPoint(filterable=True)
    postconf_builtin = RegistryPoint(filterable=True)
    postgresql_conf = RegistryPoint()
    postgresql_log = RegistryPoint(multi_output=True, filterable=True)
    prev_uploader_log = RegistryPoint()
    proc_keys = RegistryPoint()
    proc_keyusers = RegistryPoint()
    proc_netstat = RegistryPoint()
    proc_slabinfo = RegistryPoint()
    proc_snmp_ipv4 = RegistryPoint()
    proc_snmp_ipv6 = RegistryPoint()
    proc_stat = RegistryPoint()
    ps_alxwww = RegistryPoint(filterable=True)
    ps_aux = RegistryPoint(filterable=True)
    ps_auxcww = RegistryPoint()
    ps_auxww = RegistryPoint(filterable=True)
    ps_ef = RegistryPoint(filterable=True)
    ps_eo = RegistryPoint()
    ps_eo_cmd = RegistryPoint()
    pulp_worker_defaults = RegistryPoint()
    puppet_ca_cert_expire_date = RegistryPoint()
    puppet_ssl_cert_ca_pem = RegistryPoint()
    puppetserver_config = RegistryPoint(filterable=True)
    pvs_headings = RegistryPoint()
    pvs_noheadings = RegistryPoint()
    pvs_noheadings_all = RegistryPoint()
    qemu_conf = RegistryPoint()
    qemu_xml = RegistryPoint(multi_output=True)
    ql2xmaxlun = RegistryPoint()
    ql2xmqsupport = RegistryPoint()
    qpid_stat_g = RegistryPoint()
    qpid_stat_q = RegistryPoint()
    qpid_stat_u = RegistryPoint()
    qpidd_conf = RegistryPoint()
    rabbitmq_env = RegistryPoint()
    rabbitmq_logs = RegistryPoint(multi_output=True, filterable=True)
    rabbitmq_policies = RegistryPoint()
    rabbitmq_queues = RegistryPoint()
    rabbitmq_report = RegistryPoint()
    rabbitmq_report_of_containers = RegistryPoint(multi_output=True)
    rabbitmq_startup_err = RegistryPoint(filterable=True)
    rabbitmq_startup_log = RegistryPoint(filterable=True)
    rabbitmq_users = RegistryPoint()
    random_entropy_avail = RegistryPoint()
    rc_local = RegistryPoint()
    rdma_conf = RegistryPoint()
    readlink_e_etc_mtab = RegistryPoint()
    readlink_e_shift_cert_client = RegistryPoint()
    readlink_e_shift_cert_server = RegistryPoint()
    recvq_socket_buffer = RegistryPoint()
    redhat_release = RegistryPoint()
    repquota_agnpuv = RegistryPoint()
    resolv_conf = RegistryPoint()
    rhev_data_center = RegistryPoint()
    rhn_charsets = RegistryPoint()
    rhn_conf = RegistryPoint()
    rhn_entitlement_cert_xml = RegistryPoint(multi_output=True)
    rhn_hibernate_conf = RegistryPoint()
    rhn_schema_stats = RegistryPoint()
    rhn_schema_version = RegistryPoint()
    rhn_search_daemon_log = RegistryPoint(filterable=True)
    rhn_server_satellite_log = RegistryPoint(filterable=True)
    rhn_server_xmlrpc_log = RegistryPoint(filterable=True)
    rhn_taskomatic_daemon_log = RegistryPoint(filterable=False)
    rhosp_release = RegistryPoint()
    rhsm_conf = RegistryPoint()
    rhsm_katello_default_ca_cert = RegistryPoint()
    rhsm_log = RegistryPoint(filterable=True)
    rhsm_releasever = RegistryPoint()
    rhv_log_collector_analyzer = RegistryPoint()
    rndc_status = RegistryPoint()
    root_crontab = RegistryPoint()
    ros_config = RegistryPoint()
    route = RegistryPoint()
    rpm_V_packages = RegistryPoint()
    rpm_ostree_status = RegistryPoint()
    rpm_pkgs = RegistryPoint()
    rsyslog_conf = RegistryPoint(filterable=True, multi_output=True)
    samba = RegistryPoint(filterable=True)
    samba_logs = RegistryPoint(multi_output=True, filterable=True)
    sap_dev_disp = RegistryPoint(multi_output=True, filterable=True)
    sap_dev_rd = RegistryPoint(multi_output=True, filterable=True)
    sap_hana_landscape = RegistryPoint(multi_output=True)
    sap_hdb_version = RegistryPoint(multi_output=True)
    sap_host_profile = RegistryPoint(filterable=True)
    sapcontrol_getsystemupdatelist = RegistryPoint()
    saphostctl_getcimobject_sapinstance = RegistryPoint(filterable=True)
    saphostexec_status = RegistryPoint()
    saphostexec_version = RegistryPoint()
    sat5_insights_properties = RegistryPoint()
    satellite_compute_resources = RegistryPoint()
    satellite_content_hosts_count = RegistryPoint()
    satellite_core_taskreservedresource_count = RegistryPoint()
    satellite_custom_ca_chain = RegistryPoint()
    satellite_custom_hiera = RegistryPoint()
    satellite_enabled_features = RegistryPoint()
    satellite_ignore_source_rpms_repos = RegistryPoint()
    satellite_katello_repos_with_muliple_ref = RegistryPoint()
    satellite_logs_table_size = RegistryPoint()
    satellite_missed_pulp_agent_queues = RegistryPoint()
    satellite_mongodb_storage_engine = RegistryPoint()
    satellite_non_yum_type_repos = RegistryPoint()
    satellite_provision_param_settings = RegistryPoint()
    satellite_qualified_capsules = RegistryPoint()
    satellite_qualified_katello_repos = RegistryPoint()
    satellite_rhv_hosts_count = RegistryPoint()
    satellite_sca_status = RegistryPoint()
    satellite_settings = RegistryPoint()
    satellite_version_rb = RegistryPoint()
    satellite_yaml = RegistryPoint()
    sched_rt_runtime_us = RegistryPoint()
    scheduler = RegistryPoint(multi_output=True)
    scsi = RegistryPoint()
    scsi_eh_deadline = RegistryPoint(multi_output=True)
    scsi_fwver = RegistryPoint(multi_output=True)
    scsi_mod_max_report_luns = RegistryPoint()
    scsi_mod_use_blk_mq = RegistryPoint()
    sctp_asc = RegistryPoint()
    sctp_eps = RegistryPoint()
    sctp_snmp = RegistryPoint()
    sealert = RegistryPoint()
    secure = RegistryPoint(filterable=True)
    selinux_config = RegistryPoint()
    selinux_users = RegistryPoint(filterable=True)
    sendq_socket_buffer = RegistryPoint()
    sestatus = RegistryPoint()
    setup_named_chroot = RegistryPoint(filterable=True)
    smartctl = RegistryPoint(multi_output=True)
    smartpdc_settings = RegistryPoint(filterable=True)
    smbstatus_S = RegistryPoint()
    smbstatus_p = RegistryPoint()
    sockstat = RegistryPoint()
    softnet_stat = RegistryPoint()
    software_collections_list = RegistryPoint()
    sos_conf = RegistryPoint(filterable=True)
    spamassassin_channels = RegistryPoint()
    spfile_ora = RegistryPoint(multi_output=True)
    ss = RegistryPoint()
    ssh_config = RegistryPoint(filterable=True)
    ssh_config_d = RegistryPoint(multi_output=True, filterable=True)
    ssh_foreman_config = RegistryPoint(filterable=True)
    ssh_foreman_proxy_config = RegistryPoint(filterable=True)
    sshd_config = RegistryPoint(filterable=True)
    sshd_config_perms = RegistryPoint()
    sssd_config = RegistryPoint()
    sssd_logs = RegistryPoint(multi_output=True, filterable=True)
    sys_block_queue_stable_writes = RegistryPoint(multi_output=True)
    subscription_manager_facts = RegistryPoint(filterable=True)
    subscription_manager_id = RegistryPoint()
    subscription_manager_installed_product_ids = RegistryPoint(filterable=True)
    subscription_manager_list_consumed = RegistryPoint()
    subscription_manager_list_installed = RegistryPoint()
    subscription_manager_release_show = RegistryPoint()
    sudoers = RegistryPoint(multi_output=True, filterable=True)
    swift_conf = RegistryPoint()
    swift_log = RegistryPoint(filterable=True)
    swift_object_expirer_conf = RegistryPoint()
    swift_proxy_server_conf = RegistryPoint()
    sys_fs_cgroup_memory_tasks_number = RegistryPoint()
    sys_fs_cgroup_uniq_memory_swappiness = RegistryPoint()
    sys_kernel_sched_features = RegistryPoint()
    sys_vmbus_class_id = RegistryPoint(multi_output=True)
    sys_vmbus_device_id = RegistryPoint(multi_output=True)
    sysconfig_chronyd = RegistryPoint()
    sysconfig_grub = RegistryPoint()
    sysconfig_httpd = RegistryPoint()
    sysconfig_irqbalance = RegistryPoint()
    sysconfig_kdump = RegistryPoint()
    sysconfig_libvirt_guests = RegistryPoint()
    sysconfig_memcached = RegistryPoint()
    sysconfig_mongod = RegistryPoint(multi_output=True)
    sysconfig_network = RegistryPoint()
    sysconfig_nfs = RegistryPoint()
    sysconfig_ntpd = RegistryPoint()
    sysconfig_oracleasm = RegistryPoint()
    sysconfig_prelink = RegistryPoint()
    sysconfig_sshd = RegistryPoint()
    sysconfig_stonith = RegistryPoint()
    sysconfig_virt_who = RegistryPoint()
    sysctl = RegistryPoint()
    sysctl_conf = RegistryPoint()
    sysctl_conf_initramfs = RegistryPoint(multi_output=True)
    sysctl_d_conf_etc = RegistryPoint(multi_output=True)
    sysctl_d_conf_usr = RegistryPoint(multi_output=True)
    systemctl_cat_dnsmasq_service = RegistryPoint()
    systemctl_cat_rpcbind_socket = RegistryPoint()
    systemctl_list_unit_files = RegistryPoint()
    systemctl_list_units = RegistryPoint()
    systemctl_show_all_services = RegistryPoint()
    systemctl_show_all_services_with_limited_properties = RegistryPoint()
    systemctl_show_target = RegistryPoint()
    systemctl_status_all = RegistryPoint(filterable=True)
    systemd_analyze_blame = RegistryPoint()
    systemd_docker = RegistryPoint()
    systemd_logind_conf = RegistryPoint()
    systemd_openshift_node = RegistryPoint()
    systemd_system_conf = RegistryPoint()
    systemd_system_origin_accounting = RegistryPoint()
    systemid = RegistryPoint()
    systool_b_scsi_v = RegistryPoint()
    tags = RegistryPoint()
    teamdctl_config_dump = RegistryPoint(multi_output=True)
    teamdctl_state_dump = RegistryPoint(multi_output=True)
    testparm_s = RegistryPoint(filterable=True)
    testparm_v_s = RegistryPoint(filterable=True)
    thp_enabled = RegistryPoint()
    thp_use_zero_page = RegistryPoint()
    timedatectl_status = RegistryPoint()
    tmpfilesd = RegistryPoint(multi_output=True)
    tomcat_server_xml = RegistryPoint(multi_output=True)
    tomcat_vdc_fallback = RegistryPoint()
    tomcat_vdc_targeted = RegistryPoint(multi_output=True)
    tomcat_web_xml = RegistryPoint(multi_output=True)
    tuned_adm = RegistryPoint()
    tuned_conf = RegistryPoint()
    udev_fc_wwpn_id_rules = RegistryPoint(filterable=True)
    udev_persistent_net_rules = RegistryPoint()
    uname = RegistryPoint()
    up2date = RegistryPoint()
    up2date_log = RegistryPoint(filterable=True)
    uploader_log = RegistryPoint()
    uptime = RegistryPoint()
    users_count_map_selinux_user = RegistryPoint()
    usr_journald_conf_d = RegistryPoint(multi_output=True)
    var_qemu_xml = RegistryPoint(multi_output=True)
    vdo_status = RegistryPoint()
    vdsm_conf = RegistryPoint()
    vdsm_id = RegistryPoint()
    vdsm_import_log = RegistryPoint(multi_output=True, filterable=True)
    vdsm_log = RegistryPoint(filterable=True)
    vdsm_logger_conf = RegistryPoint()
    version_info = RegistryPoint()
    vgdisplay = RegistryPoint()
    vgs_headings = RegistryPoint()
    vgs_noheadings = RegistryPoint()
    vgs_noheadings_all = RegistryPoint()
    vhost_net_zero_copy_tx = RegistryPoint()
    virsh_list_all = RegistryPoint()
    virt_uuid_facts = RegistryPoint()
    virt_what = RegistryPoint()
    virt_who_conf = RegistryPoint(multi_output=True, filterable=True)
    virtlogd_conf = RegistryPoint(filterable=True)
    vma_ra_enabled = RegistryPoint()
    vmcore_dmesg = RegistryPoint(multi_output=True, filterable=True)
    vmware_tools_conf = RegistryPoint()
    vsftpd = RegistryPoint()
    vsftpd_conf = RegistryPoint(filterable=True)
    watchdog_logs = RegistryPoint(filterable=True, multi_output=True)
    wc_proc_1_mountinfo = RegistryPoint()
    x86_ibpb_enabled = RegistryPoint()
    x86_ibrs_enabled = RegistryPoint()
    x86_pti_enabled = RegistryPoint()
    x86_retp_enabled = RegistryPoint()
    xfs_info = RegistryPoint(multi_output=True)
    xfs_quota_state = RegistryPoint()
    xinetd_conf = RegistryPoint(multi_output=True)
    yum_conf = RegistryPoint()
    yum_list_available = RegistryPoint()
    yum_list_installed = RegistryPoint()
    yum_log = RegistryPoint(filterable=True)
    yum_repolist = RegistryPoint()
    yum_repos_d = RegistryPoint(multi_output=True)
    yum_updateinfo = RegistryPoint()
    yum_updates = RegistryPoint()
    zdump_v = RegistryPoint()
    zipl_conf = RegistryPoint()

    # container_specs
    container_cpu_online = RegistryPoint(multi_output=True)
    container_cpuset_cpus = RegistryPoint(multi_output=True)
    container_dotnet_version = RegistryPoint(multi_output=True)
    container_installed_rpms = RegistryPoint(multi_output=True)
    container_inspect_keys = RegistryPoint(filterable=True)
    container_mssql_api_assessment = RegistryPoint(multi_output=True)
    container_nginx_conf = RegistryPoint(multi_output=True)
    container_nginx_error_log = RegistryPoint(multi_output=True, filterable=True)
    container_ps_aux = RegistryPoint(multi_output=True, filterable=True)
    container_redhat_release = RegistryPoint(multi_output=True)
    container_vsftpd_conf = RegistryPoint(multi_output=True, filterable=True)
    containers_inspect = RegistryPoint()
