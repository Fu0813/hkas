$(document).ready(function() {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        var my_object = channel.objects.MyObject;

        document.getElementById("purchase_input").addEventListener("change",function() {
            var inputElement = document.getElementById("purchase_input");
            var inputValue = inputElement.value;
            // 检查输入是否为正整数
            var isPositiveInteger = /^\d+$/.test(inputValue);

            if (isPositiveInteger) {
                my_object.change_buycount(inputValue)
            } else {
            // 清空输入框内容或给出错误提示
                inputElement.value = "";
            // 或者可以给出其他错误提示，如弹窗等
            alert("请输入有效的正整数！");
            }
        });

        document.getElementById("serial_input").addEventListener("change",function() {
            var inputElement = document.getElementById("serial_input");
            var inputValue = inputElement.value;
            my_object.change_serial(inputValue)
        });


        my_object.signal_change_buycount.connect(function(idx) {
            var inputElement = document.getElementById("purchase_input");
            inputElement.value = idx;
        });

        my_object.signal_add_mission.connect(function(result) {
            var listItem = document.createElement("li");
            listItem.classList.add("list-group-item");
            listItem.textContent = result;

            // 添加删除按钮
            var deleteButton = document.createElement("button");
            deleteButton.classList.add("btn", "btn-danger", "float-end");
            deleteButton.textContent = "删除";
            deleteButton.addEventListener("click", function() {
                var taskList = document.getElementById("taskList");
                var index = Array.from(taskList.children).indexOf(listItem);
                my_object.delete_mission(index)
            });

            // 将删除按钮添加到列表项中
            listItem.appendChild(deleteButton);

            // 将列表项添加到任务列表中
            document.getElementById("taskList").appendChild(listItem);

        });

        my_object.signal_delete_mission.connect(function(idx) {
            var taskList = document.getElementById("taskList");
            // 获取要删除的列表项
            var listItem = taskList.children[idx];
            // 删除列表项
            listItem.remove();
        });

        my_object.signal_start_one.connect(function(idx) {
            var taskList = document.getElementById("taskList");
            // 获取要删除的列表项
            var listItem = taskList.children[idx];
            // 删除列表项
            var content = listItem.textContent.substring(0, listItem.textContent.length - 2);
            listItem.remove();
        });

        my_object.signal_change_state.connect(function(state) {
            var status = document.getElementById("state");
            status.textContent = state;
        });

        //开始运行
        document.getElementById("startBtn").addEventListener("click", function() {
            var status = document.getElementById("task_status");
            status.textContent = "队列状态：启动中";
            my_object.resume();
        });

        //暂停运行
        document.getElementById("pauseBtn").addEventListener("click", function() {
            var status = document.getElementById("task_status");
            status.textContent = "队列状态：暂停";
            my_object.pause();
        });


        document.getElementById("addTaskBtn").addEventListener("click", function() {
            // 获取选中的任务
            var selectedTask = document.getElementById("taskSelect").value;
            my_object.add_mission(selectedTask);
        });



    })
})

