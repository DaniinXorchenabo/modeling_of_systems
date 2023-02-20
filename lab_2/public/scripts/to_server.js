const get_all_input_items = (event) => {
    const send_button = document.getElementById('send_button');

    return [send_button];
};


const send_to_server = (event, task_number= "task_1") => {
    setTimeout(() => {
            const input_setup = document.getElementById('input_setup').value;
            const xhr = new XMLHttpRequest();
            xhr.open(
                'GET',
                `${document.location.protocol}//${document.location.host}/calculate/${task_number}?h=${input_setup}`,
                true
            );

            xhr.send();
            xhr.onreadystatechange = () => { // (3)
                if (xhr.readyState !== 4) return;
                if (xhr.status !== 200) {
                    console.log(xhr.status + ': ' + xhr.statusText);
                } else {
                    console.log(xhr.responseText);
                    const data = JSON.parse(xhr.responseText);
                    console.log(data);
                    // draw_formula([...Object.values(data["task1"])])
                    // get_data_for_graph([...Object.values(data["task1"])]);
                    if (data["task1"]) {
                        document.getElementById("task_1_x4").innerText = data["task1"]["target_variable"];
                        document.getElementById("task_1_delta").innerText = data["task1"]["delta"];
                        draw_graph(formatting_graph_data(data["task1"]["graph"]), "graph_task1");
                    }
                    if (data["task2"]) {
                        draw_graph(formatting_graph_data(data["task2"]["graph"]), "graph_task2");
                    }
                    if (data["task3"]) {
                        document.getElementById("task_3_x4").innerText = data["task3"]["target_variable"];
                        document.getElementById("task_3_delta").innerText = data["task3"]["delta"];
                        draw_graph(formatting_graph_data(data["task3"]["graph"]), "graph_task3");
                    }
                    // draw_graph([data["task3"]["func_graph"], data["task3"]["new_table"]], "graph_task3")

                    // document.getElementById("task_2_a").innerText = data["task2"]["lagrangian"];
                    // document.getElementById("task_2_R").innerText = data["task2"]["R_func"] + " <= " + data["task2"]["eps"];
                    // document.getElementById("task_3_D").innerText = data["task3"]["d_eps"];
                    // draw_table(data["task3"]["new_table"]);

                }
            }
        });
};

const button_handler = (event, task_number = "task_1") => {
    const dataframes = get_all_input_items(event);
    if (dataframes.some(i => i.classList.contains("error"))) {
        alert('Некоторые поля заполнены не корректно');
        return
    } else {
        send_to_server(event, task_number);
    }
}

[...document.querySelectorAll('button')].map(
    el => el.addEventListener('click', button_handler, {once: false}));

send_to_server(null, "task_2");
send_to_server(null, "task_3");