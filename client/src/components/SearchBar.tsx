import React, { useState } from "react";
import { Badge, Button, Form } from "react-bootstrap";
import { Formik } from "formik";
import "./SearchBar.css";
import closeIcon from "./closeIcon.svg";

/**
 * Split string in tags, remove non-alphanumeric characters.
 * Return last tag as head if there aren't trailing whitespaces
 * @param str string with whitespace-separated tags
 */
const splitStringInTags = (str: string): { head: string; tail: string[] } => {
  const strTrimmed = str.trim();
  const tags = strTrimmed
    .split(" ")
    .map((t) => t.replace(/\W/g, ""))
    .filter((t) => t.length > 0 && /^\w*$/.test(t));
  if (tags.length === 0) {
    return { head: "", tail: [] };
  }

  return str[str.length - 1] === " "
    ? { head: "", tail: tags }
    : { head: tags[tags.length - 1], tail: tags.slice(0, tags.length - 1) };
};

export interface ISearchBarProps {}

const SearchBar: React.FC<ISearchBarProps> = () => {
  const [tags, setTags] = useState<string[]>([]);

  const addTags = (newTags: string[]) => {
    const uniqueTags = newTags.filter((tag) => !tags.find((el) => el === tag));
    setTags(Array.from(tags).concat(uniqueTags));
  };

  return (
    <div className="SearchBar">
      <Formik
        initialValues={{ query: "" }}
        onSubmit={(values, { setSubmitting, resetForm }) => {
          setSubmitting(true);
          if (values.query.length > 0) {
            addTags([values.query]);
            resetForm();
          } else {
            alert("Send data");
          }
          setSubmitting(false);
        }}
        validateOnChange={true}
        validate={({ query }) =>
          /^\w*$/.test(query) ? {} : { query: "Invalid tag" }
        }
      >
        {({ handleSubmit, handleChange, values, errors, setFieldValue }) => (
          <Form onSubmit={handleSubmit}>
            <Form.Group className="searchbar">
              <Form.Control
                name="query"
                type="text"
                placeholder="Search for people"
                onChange={(e) => {
                  const str = e.target.value;
                  if (!str.includes(" ")) {
                    handleChange(e);
                    return;
                  }
                  const { head, tail } = splitStringInTags(str);
                  // console.log(res);
                  tail.length > 0 && addTags(tail);
                  setFieldValue("query", head);
                }}
                value={values.query}
                autoComplete="off"
              />
              <Form.Text className="text-danger">{errors.query}</Form.Text>
            </Form.Group>
            <div>
              {tags.map((el) => (
                <Badge key={el} variant="primary">
                  <div>
                    {el}
                    <span className="close-btn" aria-hidden="true">
                      <img src={closeIcon} alt="Close" />
                    </span>
                  </div>
                </Badge>
              ))}
            </div>
            <pre>
              {JSON.stringify(values, null, 2)} <br />
              {JSON.stringify(tags, null, 2)}
            </pre>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export { SearchBar };
