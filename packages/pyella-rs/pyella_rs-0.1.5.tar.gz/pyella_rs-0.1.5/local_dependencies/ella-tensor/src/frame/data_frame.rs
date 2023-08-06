use std::{fmt::Display, ops::Deref, sync::Arc};

use arrow::{
    datatypes::{Fields, Schema},
    record_batch::RecordBatch,
};
use ella_common::row::RowFormat;

use crate::{tensor_schema, NamedColumn, Shape, Tensor, TensorValue};

use super::{batch_to_columns, frame_to_batch, print::print_frames, Frame};

#[derive(Debug, Clone)]
pub struct DataFrame {
    rows: usize,
    columns: Arc<[NamedColumn]>,
}

impl DataFrame {
    pub fn col<T, S>(&self, name: &str) -> crate::Result<Tensor<T, S>>
    where
        T: TensorValue,
        S: Shape,
    {
        for col in self.columns.deref() {
            if name == col.name() {
                return crate::column::cast(col.deref());
            }
        }
        Err(crate::Error::ColumnLookup(name.to_string()))
    }

    pub fn icol<T, S>(&self, col: usize) -> crate::Result<Tensor<T, S>>
    where
        T: TensorValue,
        S: Shape,
    {
        crate::column::cast(self.columns[col].deref())
    }

    pub fn rows<R: RowFormat>(&self) -> crate::Result<R::View> {
        let batch = RecordBatch::from(self.clone());
        R::view(batch.num_rows(), &batch.schema().fields, batch.columns())
    }

    pub fn ncols(&self) -> usize {
        self.columns.len()
    }

    pub fn nrows(&self) -> usize {
        self.rows
    }

    pub fn column(&self, i: usize) -> &NamedColumn {
        &self.columns[i]
    }

    pub fn pretty_print(&self) -> impl Display + '_ {
        print_frames(&[self])
    }

    pub fn arrow_schema(&self) -> Schema {
        Schema::new(
            self.columns()
                .map(|col| {
                    Arc::new(tensor_schema(
                        col.name().to_string(),
                        col.tensor_type(),
                        col.row_shape(),
                        col.nullable(),
                    ))
                })
                .collect::<Fields>(),
        )
    }
}

impl Frame for DataFrame {
    #[inline]
    fn ncols(&self) -> usize {
        self.ncols()
    }

    #[inline]
    fn nrows(&self) -> usize {
        self.nrows()
    }

    #[inline]
    fn column(&self, i: usize) -> &NamedColumn {
        self.column(i)
    }
}

impl From<&DataFrame> for RecordBatch {
    fn from(frame: &DataFrame) -> Self {
        frame_to_batch(frame)
    }
}

impl From<DataFrame> for RecordBatch {
    fn from(frame: DataFrame) -> Self {
        frame_to_batch(&frame)
    }
}

impl TryFrom<&RecordBatch> for DataFrame {
    type Error = crate::Error;

    fn try_from(rb: &RecordBatch) -> Result<Self, Self::Error> {
        let rows = rb.num_rows();
        let columns = batch_to_columns(rb)?;
        Ok(Self { columns, rows })
    }
}

impl TryFrom<RecordBatch> for DataFrame {
    type Error = crate::Error;

    fn try_from(rb: RecordBatch) -> Result<Self, Self::Error> {
        let rows = rb.num_rows();
        let columns = batch_to_columns(&rb)?;
        Ok(Self { columns, rows })
    }
}

impl FromIterator<NamedColumn> for DataFrame {
    fn from_iter<T: IntoIterator<Item = NamedColumn>>(iter: T) -> Self {
        let columns: Arc<[NamedColumn]> = iter.into_iter().collect::<Vec<_>>().into();
        let rows = columns.first().map_or(0, |c| c.shape()[0]);
        Self { columns, rows }
    }
}
