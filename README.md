1、使用 grep -nir log > log_print.txt
2、使用 extract_log_print_patterns.py 提取出log 的种类
3、手动清理 extracted_log_print_patterns.txt 不是log的前缀
4、进入 pipeline_process_logs.py 修改 PROJECT 为代码名称，ROOT_DIR 为代码路径，然后启动当前脚本即可
