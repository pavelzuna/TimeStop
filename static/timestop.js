/* timestop.js */

function setup() {
    var stop = document.getElementById('stop');
    stop.disabled = stopped;
    stop.onclick = function () {
        stop.disabled = true;
        stopped = true;
        notice.style.display = 'block';
        ws_stop(
            function () {
                restart.disabled = false;
            },
            function (error_text) {
                restart.disabled = false;
                alert(error_text);
            }
        );
    };

    var restart = document.getElementById('restart');
    restart.disabled = !stopped;
    restart.onclick = function () {
         restart.disabled = true;
         stopped = false;
         notice.style.display = 'none';
         ws_restart(
            function () {
                stop.disabled = false;
            },
            function (error_text) {
                stop.disabled = false;
                alert(error_text);
            }
         );
    };

    var notice = document.getElementById('notice');
    if (stopped) {
         notice.style.display = 'block';
    } else {
         notice.style.display = 'none';
    }

    var time = document.getElementById('time');
    var checking = false;
    var time_value = new Date();
    setInterval(function () {
        if (!checking) {
            checking = true;
            ws_check(
                function (is_stopped, timestamp) {
                    stopped = is_stopped;
                    stop.disabled = stopped;
                    restart.disabled = !stopped;
                    time_value = new Date(timestamp * 1000);
                    if (stopped) {
                         notice.style.display = 'block';
                    } else {
                         notice.style.display = 'none';
                    }
                    checking = false;
                },
                function (error_text) {
                    alert(error_text);
                }
            );
        }
        if (!stopped) {
            time_value = new Date(time_value.getTime() + 1000);
        }
        while (time.firstChild) {
            time.removeChild(time.firstChild);
        }
        var dt = document.createTextNode(
            time_value.getUTCFullYear().toString() + '-' +
            (time_value.getUTCMonth() + 1).toString().padStart(2, '0') + '-' +
            time_value.getUTCDate().toString().padStart(2, '0'));
        time.appendChild(dt);
        time.appendChild(document.createElement('br'));
        var tm = document.createTextNode(
            time_value.getUTCHours().toString().padStart(2, '0') + ':' +
            time_value.getUTCMinutes().toString().padStart(2, '0') + ':' +
            time_value.getUTCSeconds().toString().padStart(2, '0'));
        time.appendChild(tm);
    }, 1000);
}

function _ws_base(url, on_success, on_failure) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                var data = JSON.parse(xhr.responseText);
                if (data.success) {
                    on_success(data);
                } else {
                    on_failure(data.message);
                }
            } else {
                on_failure('Communication with server failed!');
            }
        }
    }
    xhr.open('GET', url, true);
    xhr.send(null);
}

function ws_check(on_success, on_failure) {
    _ws_base('/check', function (data) {
        on_success(data.data.is_stopped, data.data.timestamp);
    }, on_failure);
}

function ws_stop(on_success, on_failure) {
    _ws_base('/stop', function (data) { on_success(); }, on_failure);
}

function ws_restart(on_success, on_failure) {
    _ws_base('/restart', function (data) { on_success(); }, on_failure);
}

/* end of file */
