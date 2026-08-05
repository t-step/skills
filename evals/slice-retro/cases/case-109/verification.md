# Verification evidence

```
$ pytest utils/test_phone.py test_signup_flow.py -v
utils/test_phone.py::test_ten_digit_number PASSED
utils/test_phone.py::test_eleven_digit_with_leading_one PASSED
utils/test_phone.py::test_garbage_input_returns_none PASSED
test_signup_flow.py::test_signup_stores_normalized_phone PASSED

4 passed in 0.02s
```
